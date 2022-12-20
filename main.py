import os
from datetime import datetime
import smtplib
import time
import requests
from dotenv import load_dotenv

load_dotenv()


MY_LAT = -19
MY_LONG = 63



def is_iss_overhead():
    """
        Sends a GET request to ISS API to locate its lat and long.
    Returns:
        bool: Returns True if user's position is within +/-5 degrees of ISS's location, otherwise returns False.
    """
    
    try:
        response = requests.get("http://api.open-notify.org/iss-now.json")

    
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)

    data = response.json()
    

    iss_latitude = data['iss_position']['latitude']
    iss_longitude = data['iss_position']['longitude']


    #Return True if user's position is within +5 or -5 degrees of the ISS position.
    if (MY_LAT-5 <= float(iss_latitude) <= MY_LAT+5) and (MY_LONG-5 <= float(iss_longitude) <= MY_LONG+5):
        return True
    
    return False


def is_night_time():
    """
        Sends a GET request to get the sunrise and sunset time of a location.
    Returns:
        bool: True if it is currently night time, False if day time.
    """

    # today = datetime.datetime.now().strftime("%Y-%m-%d")
    # parameters = {
    #      "lat": MY_LAT,
    #     "lng": MY_LONG ,
    #     "date": today,
    #     "formatted": 0
    # }

    try:
        response = requests.get(f"https://api.sunrise-sunset.org/json?lat={MY_LAT}&lng={MY_LONG}&formatted=0"
)



        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        print(error)
    

    
    data = response.json()

    sunrise = data["results"]["sunrise"]
    sunset = data["results"]["sunset"]

    # Get the current hour
    time_now = datetime.now().hour

    # Return True if it is night time
    if time_now >= int(sunset.split("T")[1].split(":")[0]) or time_now <= int(sunrise.split("T")[1].split(":")[0]):
        return True
    
    return False


# Main app logic:
# If the ISS is close to your current position and it is currently night time, notify the user
while True:
    if is_iss_overhead() and is_night_time():
        print("Look Up👆\n\nThe ISS is above you in the sky.")
        break
    else:    
        print("Unfortunately the ISS is not visible at this time, checking again in 60 seconds...")
    time.sleep(60)


# while True:
#     if is_iss_overhead() and is_night_time():
#         connection = smtplib.SMTP("smtp.gmail.com", 587) # look for the correct smtp address for your email service (gmail, outlook etc.)
#         connection.starttls()
#         connection.login(os.getenv("MY_EMAIL"), os.getenv("MY_PASSWORD"))
#         connection.sendmail(
#             from_addr=os.getenv("MY_EMAIL"),
#             to_addrs=os.getenv("MY_EMAIL"),
#             msg="Subject:Look Up👆\n\nThe ISS is above you in the sky."
#         )
#     time.sleep(60)





