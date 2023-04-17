import os
import requests
import json
from user import *

def getWeather(zipcode="47906"):
    user = User()
    zipcode = user.get_user_zipcode()
    
    token= "b2d5146e59af44d2b4d153350231402" #os.getenv("WEATHERAPI_TOKEN")
    url = "http://api.weatherapi.com/v1/current.json?key={}&q={}".format(token, zipcode)
    response = requests.get(url)
    data = json.loads(response.text)
    town = data["location"]["name"]
    temp_f = data["current"]["temp_f"]
    condition = data["current"]["condition"]["text"]
    return town, temp_f, condition

town, temp, condition = getWeather("47906")

