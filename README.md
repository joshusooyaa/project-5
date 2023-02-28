# RUSA ACP Control Time Calculator

## `db_access.py`
`db_access.py` contains two main functions, `brevet_insert` and `brevet_find`. These two functions are used to store and access the documents inside of the races collection inside of the brevets db.

`brevet_find` does the following:
1. Uses the .find() method to search all the documents inside the collection `races` and stores it as a list.
2. Returns the documents from brevetsdb as a list, in which will be turned into a JSON file in `flask_brevets.py` which is sent to the JS.

`brevet_insert` does the following:
1. Takes in the data (open times, close times, cp distances, start time, and brevet distance)
2. Before storing the data, all data from the collection is wiped (using .drop()) since the user is only allowed to save one session.
3. After wiping the data, insert_one is used to insert the data in this format:

```
"checkpoint" : str(cp),
"open_time"  : otArr[cp],
"close_time" : ctArr[cp], 
"cp_dist"    : kmArr[cp],
"start_time" : start_time,
"brevet_dist": brevet_dist
```
4. Nothing is returned from this function as `flask_brevets.py` handles all errors or exceptions.


## `acp_times.py`
`acp_times.py` Contains two main functions, `open_time` and `close_time`. These two functions calculate the open and close time of the distances provided. 

`open_time` has several rules.
1. If the distance is 0km it returns the start time of the race
2. If the distance is greater than the brevet distance, then it'll make sure to only return a time calculated up to the brevet distance (so if the distance is 305 km, it'll only calculate for 300km)
3. Otherwise, the time is calculated using distance intervals with their associated speeds. 

`close_time` follows a similar structure.
1. If the distance is 0km it returns 1 hour after the start time
2. If the distance is greater than the brevet distance then it'll make sure to return a fixed value for that brevet_distance. 
3. If the distance is <= 60 then the time is calculated by distance/20 + 1 and that is used to shift the time. 

All time is in YYYY-MM-DDTHH:MM format and must stay in this format. Both functions ensure that this format is kept by using arrow time and using the shift function the adjust the time. `brevet_start_time` is what gets shifted - as we are calculating the time based off of the beginning of the race each time. 

## `flask_brevets.py`
`flask_brevets.py` is updated to make sure the correct control distance and time is passed in so `acp_times.py` can calculate the correct times. For `flask_brevets.py` to pass a control distance, start time and brevet distance, it needs to get the information from the webpage (specifically from the JSON HTTP request) - so it uses request.args.get(). These arguments are passed in the Javascript from the getJSON request in `calc.html`. Using these arguments, they are then saved as variables in `flask_brevets.py` and are passed to the functions in `acp_times.py` to get the correct time calculations. Once this is done, the open and close times are saved and passed back to the Javascript in `calc.html` as a JSON file.

`flask_brevets.py` also handles fetch and insert requests by the user. If the user wants to save their data, as long as it's complete (there is at least one row filled in with valid data) then `flask_brevetes.py` handles this by responding to a POST request sent by the Javascript in the page -- it checks if the information passed is valid, and then sends that to `brevet_insert` to insert to the database. Once insertion is complete, as long as there were no errors along the way, it responds with a successful request and the Javascript continues. When a fetch request (GET request for fetching the data from the database), `flask_brevets.py` simply fetches the data via `brevet_find()` then returns the data as a JSON file. 

## `calc.html`
`calc.html` has been updated to make sure that the necesarry information is passed to `flask_brevets.py`. It does this by collecting the brevet distance (km) from the page, as well as the begin_date. The KM was already implemented, but that is also collected. These are then passed as arguments when sending the JSON HTTP request.
 
Once the `flask_brevets.py` sends a response back (sending the JSON back) it unpacks the information (open and close time) and updates the HTML with the open and close time that. 

`calc.html` has also now been updated to send and fetch data to/from the database.

On click of the submit button, the data is packaged up from the HTML file and sent as a POST request to `flask_brevets.py`. `flask_brevets.py` will then send back a result saying whether or not it failed. If it suceeded, all data is wiped from the screen and the user is left with the starting page (but their data has been saved). The user can now, if they wish, click on the Display button where a GET request is sent for a JSON file from `flask_brevets.py`. `flask_brevets.py`, as mentioned before, will get the data from the database and return the documents as a JSON file. The Javascript then unpack this data and updates each field with its respective data.  

-----
## Authors

Michal Young, Ram Durairajan. Updated by Ali Hassani.

Adjusted by Josh Sawyer\
jsawyer2@uoregon.edu