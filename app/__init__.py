from flask import Flask, request, jsonify, render_template
from shapely.geometry import Point, Polygon
from utils import is_number

import geopandas as gpd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return "<h1>Welcome to CodingX</h1>"

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


@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404