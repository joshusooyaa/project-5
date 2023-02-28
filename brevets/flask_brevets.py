"""
Replacement for RUSA ACP brevet time calculator
(see https://rusa.org/octime_acp.html)

"""

import flask
from flask import request
import arrow  # Replacement for datetime, based on moment.js
import acp_times  # Brevet time calculations
import config
import logging
from db_access import brevet_find, brevet_insert
import json

from datetime import timedelta

###
# Globals
###
app = flask.Flask(__name__)
CONFIG = config.configuration()

###
# Pages
###


@app.route("/")
@app.route("/index")
def index():
    app.logger.debug("Main page entry")
    return flask.render_template('calc.html')


@app.errorhandler(404)
def page_not_found(error):
    app.logger.debug("Page not found")
    return flask.render_template('404.html'), 404


###############
#
# AJAX request handlers
#   These return JSON, rather than rendering pages.
#
###############
@app.route("/_calc_times")
def _calc_times():
    """
    Calculates open/close times from miles, using rules
    described at https://rusa.org/octime_alg.html.
    Expects one URL-encoded argument, the number of miles.
    """
    app.logger.debug("Got a JSON request")
    km = request.args.get('km', 999, type=float)
    brev = request.args.get('brev', type=float) # No need for a fallback since there's always a value for brev
    start_time = request.args.get('bd', type=str)
    
    
    time = timedelta(hours=1.5)
    time2 = arrow.now()
    time2 = time + time2
    
    app.logger.debug("km={}".format(km))
    app.logger.debug("request.args: {}".format(request.args))

    open_time = acp_times.open_time(km, brev, arrow.get(start_time)).format('YYYY-MM-DDTHH:mm')
    close_time = acp_times.close_time(km, brev, arrow.get(start_time)).format('YYYY-MM-DDTHH:mm')
    app.logger.debug("open_time={}".format(open_time))
    result = {"open": open_time, "close": close_time}
    return flask.jsonify(result=result)


@app.route("/_fetch")
def _fetch_data():
    success, brevet, start, cp_data = brevet_find()
    
    if success: 
        result = {"brevet": brevet, "start_time": start, "cp_data": cp_data}
        return flask.jsonify(result=result)
    else:
        return flask.jsonify(err="No data saved")


@app.route("/_insert", methods=["POST"])
def _insert_data():
    message="Server error!" # Default error message
    
    try:
        input_json = request.json

        start_date = input_json["start_date"]
        brevet_distance = input_json["brevet_distance"]
        cp_data = input_json["items"]

        status, message = brevet_insert(brevet_distance, start_date, cp_data)
        
        return flask.jsonify(result={}, message=message, status=status)

    except:
        return flask.jsonify(result={}, message=message, status=0)

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
