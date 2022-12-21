import os
from datetime import datetime
import smtplib
import time
import requests
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()
MY_LAT = 51.450810
MY_LONG = 5.471840

def is_iss_overhead():
    """
        Sends a GET request to ISS API to locate its lat and long.
    Returns:
        bool: Returns True if user's position is within +/-5 degrees of ISS's location, otherwise returns False.
    """
    try:
        response = requests.get("http://api.open-notify.org/iss-now.json")
        responseJSON = response.json()
        print(responseJSON)
        time.sleep(1)
    except requests.exceptions.HTTPError as httpError:
        response.raise_for_status()
        raise SystemExit(httpError)

    iss_latitude =  responseJSON["iss_position"]["latitude"]
    iss_longitude =  responseJSON["iss_position"]["longitude"]

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
    #  the "formatted" parameter as 0 to get the time value in ISO format. 
    parameters = dict.fromkeys(["lat", "lng", "formatted"])
    parameters["lat"] = MY_LAT 
    parameters["lng"] = MY_LONG 
    parameters["formatted"] = 0 
    try:
        sunriseapi_response= requests.get('https://api.sunrise-sunset.org/json', params=parameters)
        sunriseapi_responseJSON = sunriseapi_response.json()
        print(sunriseapi_responseJSON)
        time.sleep(1)
    except requests.exceptions.HTTPError as httpError:
        sunriseapi_responseJSON.raise_for_status()
        raise SystemExit(httpError)
    sunrise =  sunriseapi_responseJSON["results"]["sunrise"]
    sunset =  sunriseapi_responseJSON["results"]["sunset"]
    # Get the current hour
    time_now = datetime.now().hour
 
    # Return True if it is night time
    if time_now >= int(sunset.split("T")[1].split(":")[0]) or time_now <= int(sunrise.split("T")[1].split(":")[0]):
        return True
    
    return False
 
# # Main app logic:
# # If the ISS is close to your current position and it is currently night time, notify the user

##simple method using the CMD

# while True:
#     if is_iss_overhead() and is_night_time():
#         print("Look Up👆\n\nThe ISS is above you in the sky.")
#     else:    
#         print("Unfortunately the ISS is not visible at this time, checking again in 60 seconds...")
#     time.sleep(1)



# Alternative method with SMTP library to send emails
def send_email( mail_content):
    
    sender_address = os.getenv("sender_address")
    sender_pass =  os.getenv("sender_pass")
    receiver_address =  os.getenv("receiver_address")
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'ISS is above your head!'  
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
    
while True:
    if is_iss_overhead() and is_night_time():
        send_email("Look Up👆\n\nThe ISS is above you in the sky.")  
    else:
        print("Unfortunately the ISS is not visible at this time, checking again in 60 seconds...")       
    time.sleep(60)
