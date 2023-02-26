import os 
from pymongo import MongoClient
import logging

client = MongoClient(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017")
db = client.brevetsdb
db.races.insert_one({"checkpoint": "3","open_time": "2000-12-20T20:22", "close_time": "2000-12-20T20:22", "cp_dist": "15", "start_time": "2000-12-20T20:22", "brevet_dist": "200"})
db.races.insert_one({"checkpoint": "4","open_time": "2000-12-20T20:22", "close_time": "2000-12-20T20:22", "cp_dist": "15", "start_time": "2000-12-20T20:22", "brevet_dist": "200"})


def brevet_insert(open_time, close_time, cp_dist, start_time, brevet_dist):
  # Inserts data into the brevetsdb
  pass

def brevet_find(checkpoint=0):
  """ Returns data from brevetsdb
  
  Data will be in key-value pair
  {
    "checkpoint": "cp#",
    "open_time": "YYYY-MM-DD HH:mm",
    "close_time": "YYYY-MM-DD HH:mm",   
    "cp_dist": "#km",
    
    "start_time": "YYYY-MM-DD HH:mm", 
    "brevet_dist": "#km", 
  }
  """

  data = list(db.races.find()) # Convert the all the documents to a list of dictionaries
  
  # Must pop '_id' from the dictionary since it's not needed, but also because it contains an ObjectID which is
  # not JSON serializable
  if data is not None:
    for document in data:
      document.pop('_id', None)
  
  return list(data)
