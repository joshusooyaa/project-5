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


@app.route("/_insert")
def _insert_data():
    km = request.args.getlist('km[]') # Flask changes name by attaching [] to show it's an array
    ot = request.args.getlist('otf[]', type=str)
    ct = request.args.getlist('ctf[]', type=str)
    start_date = request.args.get('start_date', type=str)
    brevet_distance = request.args.get('brevet_distance', type=str)
    
    app.logger.debug("km={}".format(km))
    app.logger.debug("otf={}".format(ot))
    app.logger.debug("ctf={}".format(ct))
    app.logger.debug("start_date={}".format(start_date))
    app.logger.debug("brev_distance={}".format(brevet_distance))
    
    response = brevet_insert(ot, ct, km, start_date, brevet_distance)
    
    return flask.jsonify(result=response)

#############

app.debug = CONFIG.DEBUG
if app.debug:
    app.logger.setLevel(logging.DEBUG)

if __name__ == "__main__":
    print("Opening for global access on port {}".format(CONFIG.PORT))
    app.run(port=CONFIG.PORT, host="0.0.0.0")
