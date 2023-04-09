import os
from datetime import datetime
import smtplib
import time
import requests
from dotenv import load_dotenv
import json

load_dotenv()


# TODO! Go to https://www.latlong.net/convert-address-to-lat-long.html and type in your address to get your location
# Store the latitude and longitude values in the variables below    
MY_LAT = 52.371712
MY_LONG = 5.221610

def is_iss_overhead():

    try:
        response = requests.get("http://api.open-notify.org/iss-now.json")
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)

    iss_pos = json.loads(response.text)
    iss_latitude = iss_pos["iss_position"]["latitude"]
    iss_longitude = iss_pos["iss_position"]["longitude"]
    
    #Return True if user's position is within +5 or -5 degrees of the ISS position.
    if (MY_LAT-5 <= float(iss_latitude) <= MY_LAT+5) and (MY_LONG-5 <= float(iss_longitude) <= MY_LONG+5):
        return True
    
    return False


def is_night_time():
    # IMPORTANT! Make sure to keep the "formatted" parameter as 0 to get the time value in ISO format. 
    parameters = {
        "lat" : MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    try:
        response = requests.get("https://api.sunrise-sunset.org/json", params = parameters)
    except requests.exceptions.RequestException as e:
        raise SystemExit(e)
    
    sun = json.loads(response.text)
    
    # sunrise and sunset times extracted from the response
    sunrise = sun["results"]["sunrise"]
    sunset = sun["results"]["sunset"]

    # Get the current hour
    time_now = datetime.now().hour
    print(int(sunset.split("T")[1].split(":")[0]))

    # Return True if it is night time
    if time_now >= int(sunset.split("T")[1].split(":")[0]) or time_now <= int(sunrise.split("T")[1].split(":")[0]):
        return True
    
    return False


# Main app logic:
# If the ISS is close to your current position and it is currently night time, notify the user
while True:
    if is_iss_overhead() and is_night_time() :
        print("Look Up👆\n\nThe ISS is above you in the sky.")
    else:    
        print("Unfortunately the ISS is not visible at this time, checking again in 60 seconds...")
    time.sleep(60)



# Alternative method with SMTP library to send emails
# If you want to use this method and send emails follow the steps below:
# create a .env file in your project directory
# add your email and password into the .env file by copying the below 2 lines and changing them with real values
# MY_EMAIL = "___YOUR_EMAIL_HERE____"
# MY_PASSWORD = "___YOUR_PASSWORD_HERE___"

# while True:
#     if is_iss_overhead() and is_night_time():
#         connection = smtplib.SMTP("__YOUR_SMTP_ADDRESS_HERE___") # look for the correct smtp address for your email service (gmail, outlook etc.)
#         connection.starttls()
#         connection.login(os.getenv("MY_EMAIL"), os.getenv("MY_PASSWORD"))
#         connection.sendmail(
#             from_addr=os.getenv("MY_EMAIL"),
#             to_addrs=os.getenv("MY_EMAIL"),
#             msg="Subject:Look Up👆\n\nThe ISS is above you in the sky."
#         )
#     time.sleep(60)
