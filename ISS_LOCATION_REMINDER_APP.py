import os
import requests
from datetime import datetime
import smtplib
import time
import load_dotenv
import json


def is_iss_overhead():

    MY_LAT = 52.336270
    MY_LONG = 5.625520
    parameters={"MY_LAT":52.336270,"MY_LONG":5.625520}
    response=requests.get("http://api.open-notify.org/iss-now.json")
    # print(response.status_code)
    data=response.json()
    x=data['iss_position']['latitude']
    y=data['iss_position']['longitude']
    # print(y)
    # print(x)
    # print(data)
    # z=response.status_code
    # print(z)
    # r=data['timestamp']
    # print(r)
    # time=datetime.fromtimestamp(r)
    # print(time)
    iss_latitude = data['iss_position']['latitude']
    iss_longitude = data['iss_position']['longitude']

        #Return True if user's position is within +5 or -5 degrees of the ISS position.
    if (MY_LAT-5 <= float(iss_latitude) <= MY_LAT+5) and (MY_LONG-5 <= float(iss_longitude) <= MY_LONG+5):
        return True
    else:
        return False

    
    
def is_night_time():

    parameters={"lat":52.336270,
                "lng":5.625520,
                "formatted": 0
        
    }
    response=requests.get("https://api.sunrise-sunset.org/json",params=parameters)
    # print(response.status_code)
    r=response.json()
    # print(r)
    sunrise=r['results']['sunrise']
    sunset=r['results']['sunset']
    # print(sunrise)
    # print(sunset)
    time_now = datetime.now().hour

    if time_now >= int(sunset.split("T")[1].split(":")[0]) or time_now <= int(sunrise.split("T")[1].split(":")[0]):
        return True
    else:
        return False

def main():
   
    
    while True:
        if is_iss_overhead() and is_night_time():
            print("Look Up👆\n\nThe ISS is above you in the sky.")
            connection = smtplib.SMTP('smtp.gmail.com', 465) # look for the correct smtp address for your email service (gmail, outlook etc.)
            connection.starttls()
            connection.login(os.getenv("iss.app.py"), os.getenv("pip50000"))
            connection.sendmail(
                from_addr=os.getenv("iss.app.py"),
                to_addrs=os.getenv("iss.app.py"),
                msg="Subject:Look Up👆\n\nThe ISS is above you in the sky."
            )
        else:    
            print("Unfortunately the ISS is not visible at this time, checking again in 60 seconds...")
            time.sleep(60)
if __name__=="__main__":
    main()
