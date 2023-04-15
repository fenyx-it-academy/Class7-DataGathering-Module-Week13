import os
from datetime import datetime
import smtplib
import time
import requests
# from dotenv import load_dotenv

# load_dotenv()


# TODO! Go to https://www.latlong.net/convert-address-to-lat-long.html and type in your address to get your location
# Store the latitude and longitude values in the variables below
MY_LAT = 51.887619
MY_LONG = 5.427876

response1=requests.get('http://api.open-notify.org/iss-now.json')
response2=requests.get(f'https://api.sunrise-sunset.org/json?lat={MY_LAT}&lng={MY_LONG}')
a=response2.json()



def is_iss_overhead():
    """
        Sends a GET request to ISS API to locate its lat and long.
    Returns:
        bool: Returns True if user's position is within +/-5 degrees of ISS's location, otherwise returns False.
    """
    
    # TODO! Make an API call (a GET request) to "http://api.open-notify.org/iss-now.json"
    # <your code here>
    response=requests.get('http://api.open-notify.org/iss-now.json')
    
    # TODO! Check for any errors by using the raise_for_status method
    # <your code here>
    result=response.json()['message']
    if(result!='success'):
        raise Exception(result)

    # TODO! Store the JSON representation of the response object in a variable
    # <your code here>
    var=response.json()

    # TODO! Parse the response object and store latitude and longitude information in variables below
    iss_latitude = var['iss_position']['latitude']
    iss_longitude = var['iss_position']['longitude']

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

    # TODO! Check out the API documentation at https://sunrise-sunset.org/api
    # Populate the parameters object below by adding the required parameters
    # IMPORTANT! Make sure to keep the "formatted" parameter as 0 to get the time value in ISO format. 
    parameters = {
        "lat" : MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    # TODO! Make an API call (a GET request) to "https://api.sunrise-sunset.org/json" along with the parameters object above.
    # Check out documentation of requests library to learn how to add parameters as a separate object in a GET request.
    # Hint: The secret info is somewhere in this page 🧐 -->  https://requests.readthedocs.io/en/latest/user/quickstart/
    # <your code here>
    # response=requests.get(f'https://api.sunrise-sunset.org/json?lat={MY_LAT}&lng={MY_LONG}')
    response = requests.get("https://api.sunrise-sunset.org/json",data=parameters)
    

    # TODO! Check for any errors by using the raise_for_status method
    # <your code here>
    response.raise_for_status()
    

    # TODO! Store the JSON representation of the response object in a variable
    # <your code here>
    var=response.json()

    # TODO! Parse the response object and store sunrise and sunset information in variables below
    sunrise = response.json()['results']['sunrise']
    sunset = response.json()['results']['sunset']

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
