from flask import Flask, request, jsonify, render_template

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
        tz_world_mp = gpd.read_file('app/data/timezones/tz_world_mp/tz_world_mp.shp')
        d = np.array(tz_world_mp['TZID'].tolist())
        e = np.unique(d)
        # e = tz_world_mp['TZID'].unique()
        f = {
            'timezones': e.tolist()
        }
        return jsonify(f)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404