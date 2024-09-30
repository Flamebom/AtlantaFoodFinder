import requests
import json
import Restaurant
"""
Google requests by name uses google smart search to try searching a value by name or cuisine also inputs into restaurant class. 
Google request class allows for the get_google_restaurants to return a list of the object Restaurant. It has two inputs, latitude and longitude.
It scans nearby for a 500 meter radius for nearby things and returns it in the list.
"""
__URL = "https://places.googleapis.com/v1/places:searchNearby"
__API_KEY = 'AIzaSyAcEWriqd7xRqv4BbS6RmP8sFUqlqqGwDU'
__URLNAME = "https://places.googleapis.com/v1/places:searchText"
def get_google_restaurants_name(name_or_cuisine):
    payload = json.dumps({
        "textQuery": name_or_cuisine,
        "maxResultCount": 10,
        "locationBias": {
            "rectangle": {
                "low": {
                    "latitude": 33.50457675495219,
                    "longitude": -84.63554645925697
                },
                "high": {
                    "latitude": 34.217961053179856,
                    "longitude": -83.76726126632337
                }
            }
        }
    })
    headers = {
        'X-Goog-Api-Key': __API_KEY,
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.primaryType,places.location,places.rating,places.nationalPhoneNumber,places.websiteUri,places.reviews',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", __URLNAME, headers=headers, data=payload)
    return format_results(response)
def get_google_restaurants(latitude, longitude):
    payload = json.dumps({
        "includedTypes": [
            "restaurant"
        ],
        "maxResultCount": 10,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": 500
            }
        }
    })
    headers = {
        'X-Goog-Api-Key': __API_KEY,
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.primaryType,places.location,places.rating,places.nationalPhoneNumber,places.websiteUri,places.reviews',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", __URL, headers=headers, data=payload)
    return format_results(response)
def format_results(response):
    rawdata = json.loads(response.text)
    list_restaurants =  (rawdata["places"])
    restaurant_output = []
    for i in range(len(list_restaurants)):
            restaurant_output.append(Restaurant.Restaurant(list_restaurants[i]))
    return restaurant_output