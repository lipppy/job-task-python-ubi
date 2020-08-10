import geopandas as gpd
import numpy as np
from shapely.geometry import Point, Polygon

class TimezoneHelper:
    error_responses = [
        {"code": 900, "message": "Error while loading geometry."},
        {"code": 901, "message": "Missing longitude."},
        {"code": 902, "message": "Missing latitude."},
        {"code": 903, "message": "Latitude is not a number."},
        {"code": 904, "message": "Longitude is not a number."},
        {"code": 905, "message": "Latitude is out of the accaptable range (between -90.0 and +90.0)."},
        {"code": 906, "message": "Longitude is out of the accaptable range (between -180.0 and +180.0)."},
        {"code": 907, "message": "Timezone was not found."},
    ]
    gdf = None

    def __init__(self):
        pass

    # Load shapefile
    def set_gdf_from_shp(self, path):
        self.gdf = gpd.read_file(path)

    def set_gdf_utc_raw(self):
        boundary = 10 ** -5 # need because neigbours boundary are the same
        left = -180.0
        right = -172.5
        utc_polygons = []
        utc_offsets = []
        for i in range(-12, 12):
            p = Polygon(
                [
                    (left, 90.0),
                    (right - boundary, 90.0),
                    (right - boundary, -90.0),
                    (left, -90.0)
                ]
            )
            utc_polygons.append(p)
            utc_offsets.append('UTC' + '{:+d}'.format(i))

            left = right
            right += 15.0 if i < 12 else 7.5

        self.gdf = gpd.GeoDataFrame()
        self.gdf['offset'] = utc_offsets
        self.gdf['geometry'] = utc_polygons
        self.gdf = self.gdf.set_geometry('geometry')

    # All available timezones's list
    def get_timezones_list(self):
        try:
            self.set_gdf_from_shp('app/data/timezones/tz_world_mp/tz_world_mp.shp')
        except:
            return self.get_error_response(900)

        tz_list = np.array(self.gdf['TZID'].tolist())
        tz_list_unique = np.unique(tz_list)
        response = {
            'timezones': tz_list_unique.tolist()
        }
        return response

    # Timezone information
    def get_timezone(self, location):
        result = None

        try:
            self.set_gdf_from_shp('app/data/timezones/tz_world_mp/tz_world_mp.shp')
        except:
            return self.get_error_response(900)

        for index, row in self.gdf.iterrows():
            # if row['TZID'] == 'uninhabited':
                # return row['geometry'].__geo_interface__
            if (location.within(row['geometry']) or location.touches(row['geometry'])) and row['TZID'] != "uninhabited":
                return {
                    "timezone": row['TZID']
                }

        return result

    # Timezone information UTC
    def get_timezone_utc(self, location):
        result = None

        try:
            self.set_gdf_from_shp('app/data/timezones/all_tz/all_tz.shp')
        except:
            return self.get_error_response(900)

        for index, row in self.gdf.iterrows():
            if row['geometry'] is not None:
                if location.within(row['geometry']) or location.touches(row['geometry']):
                    return {
                        "timezone": "UTC" + row['name']
                    }

        return result

    # Timezone information UTC (raw)
    def get_timezone_utc_raw(self, location):
        result = None

        try:
            self.set_gdf_utc_raw()
        except:
            return self.get_error_response(900)

        for index, row in self.gdf.iterrows():
            if location.within(row['geometry']) or location.touches(row['geometry']):
                return {
                    "timezone": row['offset']
                }

        return result

    # Error response
    def get_error_response(self, code):
        filtered_response = [response for response in self.error_responses if response["code"] == code]
        if len(filtered_response) == 1:
            return filtered_response[0]
        else:
            return {
                "code": code,
                "message": "Something went wrong.",
            }
