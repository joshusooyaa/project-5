"""
Nose tests for acp_times.py

Write your tests HERE AND ONLY HERE.
"""

import db_access as dba
from pymongo import MongoClient
import os
import nose    # Testing framework
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

client = MongoClient(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017")
db = client.brevetsdb

# Need to clear database before testing
db.races.drop()

def test_insert():
    # This is what is being tested
    # We're making sure that after we insert this using brevet_insert that the data is inserted
    # Answer# is expected result when we call find on the checkpoint
    # check[#] gets the dictionary that is returned from using list(*.find())
    dba.brevet_insert(['2021-01-01T01:55','2021-01-01T03:39', '2021-01-01T05:53'], ['2021-01-01T04:20', '2021-01-01T08:16', '2021-01-01T13:30'], 
                      ['65', '124', '210'], '2021-01-01T00:00', '400')
    
    answer1 = {'checkpoint': '0', 'open_time': '2021-01-01T01:55', 'close_time': '2021-01-01T04:20', 'cp_dist': '65', 'start_time': '2021-01-01T00:00', 'brevet_dist': '400'}
    answer2 = {'checkpoint': '1', 'open_time': '2021-01-01T03:39', 'close_time': '2021-01-01T08:16', 'cp_dist': '124', 'start_time': '2021-01-01T00:00', 'brevet_dist': '400'}
    answer3 = {'checkpoint': '2', 'open_time': '2021-01-01T05:53', 'close_time': '2021-01-01T13:30', 'cp_dist': '210', 'start_time': '2021-01-01T00:00', 'brevet_dist': '400'}
        
    check = list(db.races.find({"checkpoint": '0'}, {"_id": 0}))
    check2 = list(db.races.find({"checkpoint": '1'}, {"_id": 0}))
    check3 = list(db.races.find({"checkpoint": '2'}, {"_id": 0}))
    check4 = list(db.races.find({"checkpoint": '3'}, {"_id": 0})) # This shouldn't exist --> no data should exist here
    
    # These all pass if the data is inserted correctly and the database is wiped before inserting
    assert (check[0] == answer1)
    assert (check2[0] == answer2)
    assert (check3[0] == answer3)
    
    try:
        check4[0]
        assert 1 == 0
    except (IndexError, TypeError) as error:
        assert str(error) == 'list index out of range'


def test_fetch():
    db.races.drop() # Needed since we're only checking brevet_find() and past tests have added to the database
    
    db.races.insert_one({"checkpoint": '0',"open_time": "2021-01-01T01:55","close_time": "2021-01-01T04:20",   
                      "cp_dist": "65","start_time": "2021-01-01T00:00", "brevet_dist": "200" 
                      })
    db.races.insert_one({"checkpoint": '1',"open_time": "2021-01-01T03:39","close_time": "2021-01-01T08:16",   
                      "cp_dist": "124","start_time": "2021-01-01T00:00", "brevet_dist": "200" 
                      })
    db.races.insert_one({"checkpoint": '2',"open_time": "2021-01-01T05:53","close_time": "2021-01-01T13:30",   
                      "cp_dist": "210","start_time": "2021-01-01T00:00", "brevet_dist": "200" 
                      })
    
    answer1 = {'checkpoint': '0', 'open_time': '2021-01-01T01:55', 'close_time': '2021-01-01T04:20', 'cp_dist': '65', 'start_time': '2021-01-01T00:00', 'brevet_dist': '200'}
    answer2 = {'checkpoint': '1', 'open_time': '2021-01-01T03:39', 'close_time': '2021-01-01T08:16', 'cp_dist': '124', 'start_time': '2021-01-01T00:00', 'brevet_dist': '200'}
    answer3 = {'checkpoint': '2', 'open_time': '2021-01-01T05:53', 'close_time': '2021-01-01T13:30', 'cp_dist': '210', 'start_time': '2021-01-01T00:00', 'brevet_dist': '200'}
    
    check = dba.brevet_find() 
    
    assert (check[0] == answer1)
    assert (check[1] == answer2)
    assert (check[2] == answer3)
    
    try:
        check[3]
        assert 1 == 0
    except (IndexError, TypeError) as error:
        assert str(error) == 'list index out of range'


def test_integrated():
    # brevet_insert should wipe the database, so this test relies on the database being wiped
    
    dba.brevet_insert(['2021-01-01T01:55','2021-01-01T03:39', '2021-01-01T05:53'], ['2021-01-01T04:20', '2021-01-01T08:16', '2021-01-01T13:30'], 
                      ['65', '124', '210'], '2021-01-01T00:00', '200')
    
    answer1 = {'checkpoint': '0', 'open_time': '2021-01-01T01:55', 'close_time': '2021-01-01T04:20', 'cp_dist': '65', 'start_time': '2021-01-01T00:00', 'brevet_dist': '200'}
    answer2 = {'checkpoint': '1', 'open_time': '2021-01-01T03:39', 'close_time': '2021-01-01T08:16', 'cp_dist': '124', 'start_time': '2021-01-01T00:00', 'brevet_dist': '200'}
    answer3 = {'checkpoint': '2', 'open_time': '2021-01-01T05:53', 'close_time': '2021-01-01T13:30', 'cp_dist': '210', 'start_time': '2021-01-01T00:00', 'brevet_dist': '200'}

    assert (dba.brevet_find()[0] == answer1)
    assert (dba.brevet_find()[1] == answer2)
    assert (dba.brevet_find()[2] == answer3)
    
    try:
        dba.brevet_find()[3]
        assert 1 == 0
    except (IndexError, TypeError) as error:
        assert str(error) == 'list index out of range'

    # Clear after testing
    db.races.drop()   

