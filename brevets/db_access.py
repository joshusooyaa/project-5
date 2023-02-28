import os 
from pymongo import MongoClient
import logging

client = MongoClient(host=f"mongodb://{os.environ['MONGODB_HOSTNAME']}:27017")
db = client.brevetsdb
num_checkpoints = 20


def brevet_insert(brevet_dist, start_time, cp_data):
  """Inserts the data passed in, into brevetsdb. Checks for invalid data as well.
  Returns 1 on successful submit, 0 on failure (data inputted has something wrong with it)

  Args:
      otArr (str Arr): Holds the open time for each checkpoint
      ctArr (str Arr): Holds the close time for each checkpoint
      kmArr (str Arr): Holds the cp distance in KM for each checkpoint
      start_time (str): Start time of the brevet
      brevet_dist (str): Distance (in km) of the brevet
  
  """
  
  # Error checking first
  
  # If no cps created (includes ot and ct empty)
  if (len(cp_data['cp']) == 0):
    message = "No checkpoints!"
    return 0, message
  
  # Iterate through the data and ensure it's valid
  max_val = '-1'
  for i in range(len(cp_data['cp'])):
    km = cp_data['cp_dist'][i]
    ot = cp_data['ot'][i]
    ct = cp_data['ct'][i]
    
    if (ot == '' or ct == ''):
      message = 'Missing control times!'
      return 0, message
      
    # Check if data is present, but control time(s) missing
    # Also check if cps are out of order or same cp is entered
    # This could occur if km > brevet distance * 1.2
    else:
      if (int(km) <= int (max_val)):
        message = "Invalid CPs"
        return 0, message
      else:
        max_val = km  
    
  # End error checking -- we can insert now.
  
  db.races.insert_one({
                    "brevet_dist": brevet_dist, 
                    "start_time" : start_time, 
                    "cp_data"    : cp_data
                    })
  
  return 1, "Inserted!"
  

def brevet_find():
  """ Returns data from brevetsdb
  
  Data will be in key-value pair
  {
    {"brevet_dist": brevet_dist, 
     "start_time" : start_time, 
     "cp_data"    : cp_data - dict containing three arrays: cps, ot, ct, and km
  }
  """

  # Find most recently inserted document 
  data = list(db.races.find().sort("_id", -1).limit(1))
  
  # Must pop '_id' from the dictionary because it contains an ObjectID which is
  # not JSON serializable
  if len(data) > 0:
    for document in data:
      document.pop('_id', None)
  
  else:
    return 0, [], [], []
  
  brevet = data[0]["brevet_dist"]
  start = data[0]["start_time"]
  cp_data = data[0]["cp_data"]
  
  return 1, brevet, start, cp_data
