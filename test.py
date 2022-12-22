import os
from datetime import datetime
import smtplib
import time
import requests
from dotenv import load_dotenv

load_dotenv()

# MY_LAT = 52.391100
# MY_LONG = 5.250610



# def is_iss_overhead():
#     """
#         Sends a GET request to ISS API to locate its lat and long.
#     Returns:
#         bool: Returns True if user's position is within +/-5 degrees of ISS's location, otherwise returns False.
#     """
    
#     response = requests.get(url="http://api.open-notify.org/iss-now.json")
    
#     response.raise_for_status()

#     data = response.json()

#     iss_latitude = data['iss_position']['latitude']
#     iss_longitude = data['iss_position']['longitude']

#     if (MY_LAT-5 <= float(iss_latitude) <= MY_LAT+5) and (MY_LONG-5 <= float(iss_longitude) <= MY_LONG+5):
#         return True
    
#     return False

def is_night_time():
    param = {
        "lat" : 52.391100,
        "lng": 5.250610,
        "formatted": 0
    }
    res = requests.get("https://api.sunrise-sunset.org/json", params= param)
    result = res.json()
    sunrise = result['results']['sunrise']
    sunset = result['results']['sunset']
    time_now = datetime.now().hour

    if time_now >= int(sunset.split("T")[1].split(":")[0]) or time_now <= int(sunrise.split("T")[1].split(":")[0]):
      
        print('True')
    
    else:
        print('False') 

is_night_time()

    
# while True:
#     if is_iss_overhead() and is_night_time():
#         print("Look Up👆\n\nThe ISS is above you in the sky.")
#     else:    
#         print("Unfortunately the ISS is not visible at this time, checking again in 60 seconds...")
#         time.sleep(60)
