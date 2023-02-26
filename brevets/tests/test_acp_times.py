"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

import acp_times as a
import arrow

import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


# -----
# open time tests
# -----
def test_open_time_0km():
    assert arrow.get("2021-01-01T00:00") == a.open_time(0,0,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2022-01-01T00:00") == a.open_time(0,200,arrow.get("2022-01-01T00:00"))
    assert arrow.get("2023-01-01T00:00") == a.open_time(0,300,arrow.get("2023-01-01T00:00"))
    assert arrow.get("2023-01-01T00:00") == a.open_time(0,400,arrow.get("2023-01-01T00:00"))
    assert arrow.get("2023-01-01T00:00") == a.open_time(0,600,arrow.get("2023-01-01T00:00"))
    assert arrow.get("2023-01-01T00:00") == a.open_time(0,1000,arrow.get("2023-01-01T00:00"))

def test_open_time_brevet_200km():
    # Starting time of 2021-01-01 23:59 
    assert arrow.get("2021-01-01T23:59") == a.open_time(0,200,arrow.get("2021-01-01T23:59"))
    assert arrow.get("2021-01-02T00:40") == a.open_time(23,200,arrow.get("2021-01-01T23:59"))
    assert arrow.get("2021-01-02T01:47") == a.open_time(61,200,arrow.get("2021-01-01T23:59"))
    assert arrow.get("2021-01-02T03:36") == a.open_time(123,200,arrow.get("2021-01-01T23:59"))
    assert arrow.get("2021-01-02T05:52") == a.open_time(200,200,arrow.get("2021-01-01T23:59"))
    assert arrow.get("2021-01-02T05:52") == a.open_time(204,200,arrow.get("2021-01-01T23:59"))

def test_open_time_brevet_300km():
    # Starting time of 2023-05-04 11:00
    assert arrow.get("2023-05-04T11:00") == a.open_time(0,300,arrow.get("2023-05-04T11:00"))
    assert arrow.get("2023-05-04T11:58") == a.open_time(33,300,arrow.get("2023-05-04T11:00"))
    assert arrow.get("2023-05-04T14:05") == a.open_time(105,300,arrow.get("2023-05-04T11:00"))
    assert arrow.get("2023-05-04T17:06") == a.open_time(207,300,arrow.get("2023-05-04T11:00"))
    assert arrow.get("2023-05-04T19:59") == a.open_time(299,300,arrow.get("2023-05-04T11:00"))
    assert arrow.get("2023-05-04T20:00") == a.open_time(300,300,arrow.get("2023-05-04T11:00"))
    assert arrow.get("2023-05-04T20:00") == a.open_time(307,300,arrow.get("2023-05-04T11:00"))

def test_open_time_brevet_400km():
    # Starting time of 2021-01-01T00:00
    assert arrow.get("2021-01-01T00:00") == a.open_time(0,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T01:28") == a.open_time(50,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T04:25") == a.open_time(150,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T07:27") == a.open_time(250,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T10:34") == a.open_time(350,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T12:08") == a.open_time(400,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T12:08") == a.open_time(425,400,arrow.get("2021-01-01T00:00"))

def test_open_time_brevet_600km():
    # Starting time of 2021-01-01T00:00
    assert arrow.get("2021-01-01T00:00") == a.open_time(0,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T01:16") == a.open_time(43,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T05:51") == a.open_time(199,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T10:51") == a.open_time(359,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T12:16") == a.open_time(404,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T15:26") == a.open_time(499,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T18:48") == a.open_time(600,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T18:48") == a.open_time(604,600,arrow.get("2021-01-01T00:00"))

def test_open_time_brevet_1000km():
    # Starting time of 2021-01-01T00:00
    assert arrow.get("2021-01-01T00:00") == a.open_time(0,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T01:16") == a.open_time(43,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T05:51") == a.open_time(199,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T10:51") == a.open_time(359,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T12:16") == a.open_time(404,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T15:26") == a.open_time(499,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T18:48") == a.open_time(600,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T18:57") == a.open_time(604,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T01:31") == a.open_time(788,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T03:31") == a.open_time(844,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T07:39") == a.open_time(960,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T09:05") == a.open_time(1000,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T09:05") == a.open_time(1024,1000,arrow.get("2021-01-01T00:00"))


# -----
# close_time tests
# -----
def test_close_time_0km():
    assert arrow.get("2021-01-01T01:00") == a.close_time(0,0,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2022-02-02T00:00") == a.close_time(0,200,arrow.get("2022-02-01T23:00"))
    assert arrow.get("2023-01-01T01:00") == a.close_time(0,300,arrow.get("2023-01-01T00:00"))
    assert arrow.get("2023-01-01T01:00") == a.close_time(0,400,arrow.get("2023-01-01T00:00"))
    assert arrow.get("2023-01-01T02:00") == a.close_time(0,600,arrow.get("2023-01-01T01:00"))
    assert arrow.get("2023-01-01T03:00") == a.close_time(0,1000,arrow.get("2023-01-01T02:00"))

def test_close_time_200km():
    assert arrow.get("2021-01-01T01:00") == a.close_time(0,200,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T03:27") == a.close_time(49,200,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T08:00") == a.close_time(120,200,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T13:30") == a.close_time(200,200,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T13:30") == a.close_time(207,200,arrow.get("2021-01-01T00:00"))

def test_close_time_300km():
    assert arrow.get("2021-01-01T01:00") == a.close_time(0,300,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T03:27") == a.close_time(49,300,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T08:00") == a.close_time(120,300,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T13:20") == a.close_time(200,300,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T13:48") == a.close_time(207,300,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T20:00") == a.close_time(300,300,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T20:00") == a.close_time(314,300,arrow.get("2021-01-01T00:00"))

def test_close_time_400km():
    assert arrow.get("2021-01-01T01:00") == a.close_time(0,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T03:27") == a.close_time(49,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T08:00") == a.close_time(120,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T13:20") == a.close_time(200,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T13:48") == a.close_time(207,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T20:00") == a.close_time(300,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T20:56") == a.close_time(314,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T03:00") == a.close_time(400,400,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T03:00") == a.close_time(421,400,arrow.get("2021-01-01T00:00"))

def test_close_time_600km():
    assert arrow.get("2021-01-01T01:00") == a.close_time(0,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T03:27") == a.close_time(49,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T08:00") == a.close_time(120,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T13:20") == a.close_time(200,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T13:48") == a.close_time(207,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T20:00") == a.close_time(300,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T20:56") == a.close_time(314,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T02:40") == a.close_time(400,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T04:04") == a.close_time(421,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T13:00") == a.close_time(555,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T16:00") == a.close_time(600,600,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T16:00") == a.close_time(642,600,arrow.get("2021-01-01T00:00"))

def test_close_time_1000km():
    assert arrow.get("2021-01-01T01:00") == a.close_time(0,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T01:36") == a.close_time(12,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T08:00") == a.close_time(120,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T13:20") == a.close_time(200,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T13:48") == a.close_time(207,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T20:00") == a.close_time(300,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-01T20:56") == a.close_time(314,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T02:40") == a.close_time(400,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T04:04") == a.close_time(421,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T13:00") == a.close_time(555,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T16:00") == a.close_time(600,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-02T19:41") == a.close_time(642,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-03T08:27") == a.close_time(788,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-03T13:11") == a.close_time(842,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-03T19:08") == a.close_time(910,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-04T03:00") == a.close_time(1000,1000,arrow.get("2021-01-01T00:00"))
    assert arrow.get("2021-01-04T03:00") == a.close_time(1050,1000,arrow.get("2021-01-01T00:00"))





