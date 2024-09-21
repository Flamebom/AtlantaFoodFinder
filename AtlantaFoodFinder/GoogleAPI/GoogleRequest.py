import requests
import json

url = "https://places.googleapis.com/v1/places:searchNearby"

payload = json.dumps({
  "includedTypes": [
    "restaurant"
  ],
  "maxResultCount": 10,
  "locationRestriction": {
    "circle": {
      "center": {
        "latitude": 45.55860601168696,
        "longitude": -122.86519658540723
      },
      "radius": 500
    }
  }
})
headers = {
  'X-Goog-Api-Key': 'AIzaSyAn2GEz9YyAxynT77ezXbhIF9Ua9iy2ABk',
  'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.primaryType,places.location,places.rating,places.nationalPhoneNumber,places.websiteUri,places.reviews',
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
