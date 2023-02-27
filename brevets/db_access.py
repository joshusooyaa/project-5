import os 
from pymongo import MongoClient
import logging

client = MongoClient(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017")
db = client.brevetsdb
num_checkpoints = 20

for cp in range(num_checkpoints):
  db.races.insert_one({
                      "checkpoint": str(cp),
                      "open_time": "",
                      "close_time": "",   
                      "cp_dist": "",
                      "start_time": "2021-01-01T00:00", 
                      "brevet_dist": "200" 
                      })


def brevet_insert(otArr, ctArr, kmArr, start_time, brevet_dist):
  """Inserts the data passed in, into brevetsdb

  Args:
      otArr (str Arr): Holds the open time for each checkpoint
      ctArr (str Arr): Holds the close time for each checkpoint
      kmArr (str Arr): Holds the cp distance in KM for each checkpoint
      start_time (str): Start time of the brevet
      brevet_dist (str): Distance (in km) of the brevet
  """
  
  for cp in range(len(kmArr)):
    db.races.update_one({"checkpoint": str(cp)},
                        {"$set": {"open_time"  : otArr[cp],
                                  "close_time" : ctArr[cp],
                                  "cp_dist"    : kmArr[cp],
                                  "start_time" : start_time, 
                                  "brevet_dist": brevet_dist}})

  response = {"response": "saved"}
     
  return response

def brevet_find(checkpoint=0):
  """ Returns data from brevetsdb
  
  Data will be in key-value pair
  {
    {"checkpoint": "cp#",
    "open_time": "YYYY-MM-DD HH:mm",
    "close_time": "YYYY-MM-DD HH:mm",   
    "cp_dist": "#km",
    
    "start_time": "YYYY-MM-DD HH:mm", 
    "brevet_dist": "#km"  
  }
  """

  data = list(db.races.find().limit(20)) # Convert the all the documents to a list of dictionaries
  
  # Must pop '_id' from the dictionary since it's not needed, but also because it contains an ObjectID which is
  # not JSON serializable
  if data is not None:
    for document in data:
      document.pop('_id', None)
  
  return list(data)
