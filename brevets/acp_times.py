"""
Open and close time calculations
for ACP-sanctioned brevets
following rules described at https://rusa.org/octime_alg.html
and https://rusa.org/pages/rulesForRiders
"""
import arrow

#  You MUST provide the following two functions
#  with these signatures. You must keep
#  these signatures even if you don't use all the
#  same arguments.
#

# km: hrs
times_dict = { 
   200: 13.5,
   300: 20,
   400: 27,
   600: 40,
   1000: 75 
}

def open_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
       brevet_dist_km: number, nominal distance of the brevet
           in kilometers, which must be one of 200, 300, 400, 600,
           or 1000 (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control open time.
       This will be in the same time zone as the brevet start time.
    """
    max_distance = False
    
    if control_dist_km == 0: 
       return brevet_start_time
    
    if control_dist_km >= brevet_dist_km * 1.2:
       return "ERROR"
    
    if (control_dist_km > brevet_dist_km):
       max_distance = True
       
    time = 0
    interval = 0
    max_interval = 3
    max_speed = [34, 32, 30, 28]
    distance_intervals = [200, 200, 200, 400]
    value_to_divide = 0
    
    # First check if control distance is farther than the interval distance
    # If the interval distance is less, then divide that distance by the speed for that interval
    # If the control distance is less than the distance_interval, first check if brevet distance is 300, and this is a max_distance
    #   - If it is, we want to make sure we divide using 100, and not 101, 102, etc.  
    # If neither of these cases are true, we check if this is a max_distance - if this is the case, we don't want to add more time for distances over the max brevet distance, so break
    # Else - We divide the reamining control_distance  
    # 
    # Control_distance is subtracted by the distance interval each time it's added
    
    while (control_dist_km > 0):
       if (control_dist_km > distance_intervals[interval]):
          value_to_divide = distance_intervals[interval]
       elif (max_distance and brevet_dist_km == 300):
          value_to_divide = 100
       elif max_distance:
          break # Break while loop since all time addition has been done (don't want to add any more for distances over the brevet distance)
       else:
         value_to_divide = control_dist_km
      
       time += (value_to_divide/max_speed[interval])
       control_dist_km -= distance_intervals[interval] 
       
       # I want to mention I could rewrite this so once max_interval is passed the loop breaks since that'd make more sense
       # However, the implementation as it is still works - just isn't as clean as I'd like
       if (interval != max_interval): # Preventing indexing error - (since some control_distances can go over the brevet_dist)
         interval += 1
    
    seconds = convert_time(time) # Make sure it rounds up if needed
    
    return brevet_start_time.shift(seconds=+seconds)
        


def close_time(control_dist_km, brevet_dist_km, brevet_start_time):
    """
    Args:
       control_dist_km:  number, control distance in kilometers
          brevet_dist_km: number, nominal distance of the brevet
          in kilometers, which must be one of 200, 300, 400, 600, or 1000
          (the only official ACP brevet distances)
       brevet_start_time:  An arrow object
    Returns:
       An arrow object indicating the control close time.
       This will be in the same time zone as the brevet start time.
    """
        
    # First check three things
    # 1. Is the control distance 0? 
    # 2. Is the control_distance larger than the brevet_distance? 
    # 3. Is the control_distance less than 60? 
    
    if control_dist_km == 0: 
       return brevet_start_time.shift(hours=+1)
    
    if control_dist_km >= brevet_dist_km * 1.2:
       return "ERROR"
    
    if control_dist_km >= brevet_dist_km:
       shift_time = times_dict[brevet_dist_km]
       return brevet_start_time.shift(hours=+shift_time)
    
    if control_dist_km <= 60:
       shift_time = control_dist_km/20 + 1
       return brevet_start_time.shift(hours=+shift_time)
    
    time = 0
    interval = 0
    max_interval = 1
    max_speed = [15, 11.428]
    distance_intervals = [600, 400]
    while (control_dist_km > 0):    
       if (control_dist_km > distance_intervals[interval]):
          value_to_divide = distance_intervals[interval]
       else:
          value_to_divide = control_dist_km
          
       time += (value_to_divide/max_speed[interval])
       control_dist_km -= distance_intervals[interval] 
       
       if (interval != max_interval): 
         interval += 1
         
       
    seconds = convert_time(time) # Make sure it rounds up if needed
    
    return brevet_start_time.shift(seconds=+seconds)
 

def convert_time(time):
    seconds = 3600 * time
    if (seconds % 60 >= 30): # Check if rounding up is needed
       seconds_to_add = 60 - (seconds % 60)
       seconds += seconds_to_add
    else: # Round down
       seconds -= (seconds % 60)
    return seconds  