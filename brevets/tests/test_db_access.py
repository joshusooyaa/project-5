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


# Data is stored as {'brevet_dist': '', 'start_time': '', 'cp_data': {'cp': [], 'ot': [], 'ct': [], 'cp_dist': []}}
# Simply create an answer with this template, and then fill in -- then break it up into parts and use dba.brevet_insert
# After dba.brevet_insert() use .find() and ensure that the data has been stored correctly
def test_insert():
    # this is what we should get back when we run .find() on the latest inserted item
    # we'll use the information from this to insert
    answer = {'brevet_dist': '200', 'start_time': '2021-01-01T00:00', 'cp_data': {'cp': ['0','1','2'], 'ot': ['2021-01-01T01:37','2021-01-01T02:56','2021-01-01T05:53'], 'ct': ['2021-01-01T03:45','2021-01-01T06:40','2021-01-01T13:30'], 'cp_dist': ['55', '100', '200']}}
    
    brevet_distance = answer['brevet_dist']
    start_time = answer['start_time']
    cp_data = answer['cp_data']
    dba.brevet_insert(brevet_distance, start_time, cp_data)
            
    check = list(db.races.find().sort("_id", -1).limit(1))
    if check:
        check[0].pop('_id', None)
    
    print(check[0])
    print(answer)
    
    assert (check[0] == answer)

# Check if data is stored when another document is added (test_insert makes it so races has a document in it)
def test_insert2():
    answer = {'brevet_dist': '400', 'start_time': '2021-01-01T00:00', 'cp_data': {'cp': ['0','1','2','3'], 'ot': ['2021-01-01T01:37','2021-01-01T02:56','2021-01-01T05:53','2021-01-01T12:08'], 'ct': ['2021-01-01T03:45','2021-01-01T06:40','2021-01-01T13:20','2021-01-02T03:00'], 'cp_dist': ['55', '100', '200', '400']}}
    
    brevet_distance = answer['brevet_dist']
    start_time = answer['start_time']
    cp_data = answer['cp_data']
    dba.brevet_insert(brevet_distance, start_time, cp_data)
            
    check = list(db.races.find().sort("_id", -1).limit(1))
    if check:
        check[0].pop('_id', None)
    
    print(check[0])
    print(answer)
    
    assert (check[0] == answer)
    

# Fetch fetches the data and returns it as tuple of 'success', 'brevet_distance', 'start_date', 'cp_data'
def test_fetch():
    insert = {'brevet_dist': '200', 'start_time': '2021-01-01T00:00', 'cp_data': {'cp': ['0','1','2'], 'ot': ['2021-01-01T01:37','2021-01-01T02:56','2021-01-01T05:53'], 'ct': ['2021-01-01T03:45','2021-01-01T06:40','2021-01-01T13:30'], 'cp_dist': ['55', '100', '200']}}

    db.races.insert_one(insert)
        
    check = dba.brevet_find() 
    
    assert(check[0] == 1) # Successful fetch
    assert(check[1] == insert['brevet_dist'])
    assert(check[2] == insert['start_time'])
    assert(check[3] == insert['cp_data'])

def test_fetch2():
    insert = {'brevet_dist': '400', 'start_time': '2021-01-01T00:00', 'cp_data': {'cp': ['0','1','2','3'], 'ot': ['2021-01-01T01:37','2021-01-01T02:56','2021-01-01T05:53','2021-01-01T12:08'], 'ct': ['2021-01-01T03:45','2021-01-01T06:40','2021-01-01T13:20','2021-01-02T03:00'], 'cp_dist': ['55', '100', '200', '400']}}
    
    db.races.insert_one(insert)
    
    check = dba.brevet_find() 
    
    assert(check[0] == 1) # Successful fetch
    assert(check[1] == insert['brevet_dist'])
    assert(check[2] == insert['start_time'])
    assert(check[3] == insert['cp_data'])

# Test on an empty races collection
def test_fetch3():
    db.races.drop() # Empty the database
    check = dba.brevet_find()
    assert(check[0] == 0) # Unsuccessful fetch 


def test_integrated():
    insert = {'brevet_dist': '1000', 'start_time': '2021-01-01T00:00', 'cp_data': {'cp': ['0','1','2'], 'ot': ['2021-01-01T01:37','2021-01-01T02:56','2021-01-01T05:53'], 'ct': ['2021-01-01T03:45','2021-01-01T06:40','2021-01-01T13:30'], 'cp_dist': ['55', '100', '200']}}
    
    brevet_distance = insert['brevet_dist']
    start_time = insert['start_time']
    cp_data = insert['cp_data']
    dba.brevet_insert(brevet_distance, start_time, cp_data)
    check = dba.brevet_find()
    
    assert(check[0] == 1) # Successful fetch
    assert(check[1] == insert['brevet_dist'])
    assert(check[2] == insert['start_time'])
    assert(check[3] == insert['cp_data'])
    
    # Clear races collection after testing
    db.races.drop()
    
    


