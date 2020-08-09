from flask import Flask, request, jsonify, render_template
from shapely.geometry import Point, Polygon
from app.utils import is_number

import geopandas as gpd
import numpy as np

app = Flask(__name__)

# app.config.from_object('config.ProductionConfig')
app.config.from_object('config.DevelopmentConfig')

@app.route('/')
def home():
    return render_template('public/home.html')

@app.route('/timezones', methods=['GET'])
def api_timezones():
    # No location data available: Display all available timezones's list
    if 'lat' not in request.args and 'lon' not in request.args:
        # Load Timezone shapefile
        tz_world_mp = gpd.read_file('app/data/timezones/tz_world_mp/tz_world_mp.shp')
        d = np.array(tz_world_mp['TZID'].tolist())
        e = np.unique(d)
        # e = tz_world_mp['TZID'].unique()
        f = {
            'timezones': e.tolist()
        }
        return jsonify(f)
    # Missing longitude
    elif 'lat' in request.args and 'lon' not in request.args:
        return {
            "code": "Missing longitude."
        }
    # Missing latitude
    elif 'lat' not in request.args and 'lon' in request.args:
        return {
            "code": "Missing latitude."
        }
    # Both location data available
    elif 'lat' in request.args and 'lon' in request.args:
        # Check whether lat is number
        if is_number(request.args['lat']):
            lat = float(request.args['lat'])
        else:
            return {
                "code": "Latitude is not a number."
            }
        # Check whether lon is number
        if is_number(request.args['lon']):
            lon = float(request.args['lon'])
        else:
            return {
                "code": "Longitude is not a number."
            }
        # Check whether lat is between -90.0 and +90.0
        if abs(lat) < 0.0 or abs(lat) > 90.0:
            return {
                "code": "Latitude is out of range."
            }
        # Check whether lon is between -180.0 and +180.0
        if abs(lon) < 0.0 or abs(lon) > 180.0:
            return {
                "code": "Longitude is out of range."
            }

        # Location data passed check process
        location = Point(lon, lat)

        # Load Timezone shapefile
        tz_world_mp = gpd.read_file('app/data/timezones/tz_world_mp/tz_world_mp.shp')

        for index, row in tz_world_mp.iterrows():
            # if row['TZID'] == 'uninhabited':
                # return row['geometry'].__geo_interface__
            if location.within(row['geometry']) and row['TZID'] != "uninhabited":
                return {
                    "timezone": row['TZID']
                }

        # If we reach this point then our point was not found in tz_world_mp - Check UTC
        # 1. Arg: utccheck = raw - Basic UTC - Polygons set manually
        # 2. No utccheck arg or utcheck arg not equal raw
        if 'utccheck' in request.args and request.args['utccheck'] == 'raw':
            left = -180.0
            right = -172.5
            utc_polygons = []
            utc_offsets = []
            for i in range(-12, 12):
                p = Polygon(
                    [
                        (left, 90.0),
                        (right, 90.0),
                        (right, -90.0),
                        (left, -90.0)
                    ]
                )
                utc_polygons.append(p)
                utc_offsets.append('UTC' + '{:+d}'.format(i))

                left = right
                right += 15.0 if i < 12 else 7.5

            utc_tz = gpd.GeoDataFrame()
            utc_tz['offset'] = utc_offsets
            utc_tz['geometry'] = utc_polygons
            utc_tz = utc_tz.set_geometry('geometry')

            for index, row in utc_tz.iterrows():
                if location.within(row['geometry']):
                    return {
                        "timezone": row['offset']
                    }
        else:
            # Load UTC Timezone shapefile
            all_tz = gpd.read_file('app/data/timezones/all_tz/all_tz.shp')

            for index, row in all_tz.iterrows():
                if row['geometry'] is not None:
                    if location.within(row['geometry']):
                        return {
                            "timezone": "UTC" + row['name']
                        }

@app.errorhandler(404)
def page_not_found(e):
    return render_template('public/error.html'), 404