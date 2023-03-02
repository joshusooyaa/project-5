# RUSA ACP Control Time Calculator

## **How to run**
Simply run the command `docker-compose up --build -d` or remove `-d` if you wish to look at the logs of the server. You can then connect to your local host via localhost:5001 and you can connect to the page. To shut down the server and the webpage, use docker-compose down. This will close the two containers (mongo db and the webpage) and shutdown the connection. As one might expect, this also wipes the database since the container that the mongo image is in has been stopped, but more importantly, removed.

## `db_access.py`
`db_access.py` contains two main functions, `brevet_insert` and `brevet_find`. These two functions are used to store and access the documents inside of the races collection inside of the brevets db.

`brevet_find` does the following:
1. Uses the .find().limit(1) method to find the latest insertion since currently we are only implementing the ability to load the most recently saved data.
2. Returns the document from brevetsdb.races as a list, in which will be turned into a JSON file in `flask_brevets.py` which is sent to the JS.

`brevet_insert` does the following:
1. Takes in the data and ensures it's proper (ex: missing control times for a cp)
2. Data is then inserted into the races collection inside of brevetsdb using insert_one -- data that is inserted is as follows:
```
"brevet_dist" : brevet distance,
"start_time"  : start time of brevet,
"cp_data"     : cp_data - dict containing three arrays: cps, ot, ct, and km
```
4. A tuple is returned (success, message) where success is either 0 or 1 indicating if the information was stored or not, and a message for if it was inserted, or for what error occured.


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

`flask_brevets.py` also handles fetch and insert requests by the user. If the user wants to save their data, as long as it's complete (there is at least one row filled in with valid data) then `flask_brevetes.py` handles this by responding to a POST request sent by the Javascript in the page. It takes the information and packages it up correctly and calls `brevet_insert` with it to insert to the database. Once insertion is complete, as long as there were no errors along the way, it responds with a successful request and the Javascript continues. When a fetch request (GET request for fetching the data from the database), `flask_brevets.py` simply fetches the data via `brevet_find()` then returns the data as a JSON file where the JS handles unpacks it and updates the page (without refreshing). 

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
