import requests
import json
from . import Restaurant
# import Restaurant
"""
Google requests by name uses google smart search to try searching a value by name or cuisine also inputs into restaurant class. 
Google request class allows for the get_google_restaurants to return a list of the object Restaurant. It has two inputs, latitude and longitude.
It scans nearby for a 500 meter radius for nearby things and returns it in the list.
"""
__URL = "https://places.googleapis.com/v1/places:searchNearby"
__API_KEY = ''
__URLNAME = "https://places.googleapis.com/v1/places:searchText"
def get_google_restaurants(latitude,longitude,name_or_cuisine='restaurants',distance = 10000,min_rating =0.0):
    payload = json.dumps({
        "textQuery": name_or_cuisine,
        "maxResultCount": 15,
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": distance
            }
        },
        "minRating": min_rating,
        "rankPreference": "DISTANCE"
    })
    headers = {
        'X-Goog-Api-Key': __API_KEY,
        'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.primaryType,places.location,places.rating,places.nationalPhoneNumber,places.websiteUri,places.reviews',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", __URLNAME, headers=headers, data=payload)
    return format_results(response)

def format_results(response):
    rawdata = json.loads(response.text)
    list_restaurants = rawdata.get("places", [])
    restaurant_output = []
    for i in range(len(list_restaurants)):
        restaurant_output.append(Restaurant.Restaurant(list_restaurants[i]))
    return restaurant_output