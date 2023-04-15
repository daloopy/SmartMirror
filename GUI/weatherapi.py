import os
import requests
import json
from user import *

def getWeather():
    user = User()
    zipcode = user.get_user_zipcode()
    token= "b2d5146e59af44d2b4d153350231402" #os.getenv("WEATHERAPI_TOKEN")
    url = "http://api.weatherapi.com/v1/current.json?key={}&q={}".format(token, zipcode)
    response = requests.get(url)

    if(response.ok):
        data = json.loads(response.text)
        print("response 200")
        town = data['location']["name"]
        temp_f = data["current"]["temp_f"]
        condition = data["current"]["condition"]["text"]

    else:
        town = "invalid zipcode"
        temp_f = "-"
        condition = "-"

    return town, temp_f, condition

#town, temp, condition = getWeather()
#print(town, temp, condition)


