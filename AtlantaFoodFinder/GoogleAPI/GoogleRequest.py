import requests
import json
import Restaurant
"""
Google request class allows for the get_google_restaurants to return a list of the object Restaurant. It has two inputs, latitude and longitude.
It scans nearby for a 500 meter radius for nearby things and returns it in the list.
"""
__URL = "https://places.googleapis.com/v1/places:searchNearby"
__API_KEY = 'AIzaSyAn2GEz9YyAxynT77ezXbhIF9Ua9iy2ABk'


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
    rawdata = json.loads(response.text)
    list_restaurants =  (rawdata["places"])
    restaurant_output = []
    for i in range(len(list_restaurants)):
            restaurant_output.append(Restaurant.Restaurant(list_restaurants[i]))
    return restaurant_output
