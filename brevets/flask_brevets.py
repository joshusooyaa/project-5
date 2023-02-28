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
    data = brevet_find()

    if data is not None:
        return flask.jsonify(result=data)
    else:
        return flask.jsonify(err="No data saved")


@app.route("/_insert", methods=["POST"])
def _insert_data():
    message="Server error!" # Default error message
    
    try:
        input_json = request.json
        
        km = input_json["km"]
        ot = input_json["otf"]
        ct = input_json["ctf"]
        start_date = input_json["start_date"]
        brevet_distance = input_json["brevet_distance"]
        
        # Check if any checkpoints are submitted ()
        if (all(x == '' for x in km)):
            message = "No checkpoint distances!"
            raise Exception(message)
        
        # Check if control times are all emtpy (no info to submit) -- This will occur if brev_dist * 1.2 <= km
        if (all(x == '' for x in ot) or all(y == '' for y in ct)):
            message = "No control times!"
            raise Exception(message)
        
        app.logger.debug("km={}".format(len(km)))
        app.logger.debug("otf={}".format(ot))
        app.logger.debug("ctf={}".format(ct))
        app.logger.debug("start_date={}".format(start_date))
        app.logger.debug("brev_distance={}".format(brevet_distance))

        brevet_insert(ot, ct, km, start_date, brevet_distance)
        
        return flask.jsonify(result={"success": "1"}, message="Inserted!", status=1)
    
    except:
        return flask.jsonify(result={}, message=message, status=0)

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
