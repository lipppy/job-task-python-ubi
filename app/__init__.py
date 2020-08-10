from flask import Flask, request, jsonify, render_template
from shapely.geometry import Point
from app.utils import is_number
from app.timezoneapi import TimezoneHelper

app = Flask(__name__)

# app.config.from_object('config.ProductionConfig')
app.config.from_object('config.DevelopmentConfig')

@app.route('/')
def home():
    return render_template('public/home.html')

@app.route('/timezones', methods=['GET'])
def api_timezones():
    tzh = TimezoneHelper()
    # No location data available: Display all available timezones's list
    if 'lat' not in request.args and 'lon' not in request.args:
        return jsonify(tzh.get_timezones_list())
    # Missing longitude
    elif 'lat' in request.args and 'lon' not in request.args:
        return jsonify(tzh.get_error_response(901))
    # Missing latitude
    elif 'lat' not in request.args and 'lon' in request.args:
        return jsonify(tzh.get_error_response(902))
    # Both location data available
    elif 'lat' in request.args and 'lon' in request.args:
        # Check whether lat is number
        if is_number(request.args['lat']):
            lat = float(request.args['lat'])
        else:
            return jsonify(tzh.get_error_response(903))

        # Check whether lon is number
        if is_number(request.args['lon']):
            lon = float(request.args['lon'])
        else:
            return jsonify(tzh.get_error_response(904))

        # Check whether lat is between -90.0 and +90.0
        if abs(lat) < 0.0 or abs(lat) > 90.0:
            return jsonify(tzh.get_error_response(905))

        # Check whether lon is between -180.0 and +180.0
        if abs(lon) < 0.0 or abs(lon) > 180.0:
            return jsonify(tzh.get_error_response(906))

        # Location data passed, next phase getting timezone
        location = Point(lon, lat)

        # Check timezone
        response = tzh.get_timezone(location)
        if response is not None:
            return jsonify(response)

        # If we reach this point then our point was not found in tz_world_mp - Check UTC
        # 1. Arg: utccheck = raw - Basic UTC - Polygons set manually
        # 2. No utccheck arg or utcheck arg not equal raw
        if 'utccheck' in request.args and request.args['utccheck'] == 'raw':
            response = tzh.get_timezone_utc_raw(location)
        else:
            response = tzh.get_timezone_utc(location)

        if response is not None:
            return jsonify(response)
        else:
            return jsonify(tzh.get_error_response(907))



@app.errorhandler(404)
def page_not_found(e):
    return render_template('public/error.html'), 404