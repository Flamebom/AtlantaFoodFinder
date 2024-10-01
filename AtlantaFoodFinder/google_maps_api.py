import googlemaps
from restaurant import Restaurant

class GoogleMapsAPI:
    def __init__(self, api_key):
        self.gmaps = googlemaps.Client(key=api_key)

    def get_nearby_restaurants(self, location, radius=1500):
        try:
            places_result = self.gmaps.places_nearby(location=location, radius=radius, type='restaurant')
            restaurants = []

            for place in places_result['results']:
                name = place['name']
                rating = place.get('rating')
                address = place.get('vicinity')
                place_id = place['place_id']

                lat = place['geometry']['location']['lat']
                lng = place['geometry']['location']['lng']

                details = self.get_place_details(place_id)

                cuisine = self.infer_cuisine(name)

                restaurant = Restaurant(
                    name=name,
                    rating=rating,
                    address=address,
                    latitude=lat,
                    longitude=lng,
                    phone=details.get('formatted_phone_number'),
                    opening_hours=details.get('opening_hours', {}).get('weekday_text'),
                    menu=details.get('menu'),
                    website=details.get('website'),
                    cuisine=cuisine,
                    gmaps_client=self.gmaps
                )
                restaurants.append(restaurant)
            return restaurants

        except googlemaps.exceptions.ApiError as e:
            print(f"API error occurred: {e}")
            return []

    def get_place_details(self, place_id):
        try:
            details = self.gmaps.place(place_id=place_id, fields=[
                'name', 'formatted_phone_number', 'opening_hours', 'menu', 'website'
            ])
            return details.get('result', {})
        except googlemaps.exceptions.ApiError as e:
            print(f"API error occurred while fetching details: {e}")
            return {}

    def infer_cuisine(self, name):
        cuisine_keywords = {
            'Sushi': 'Japanese',
            'Pizza': 'Italian',
            'Burger': 'American',
            'Tacos': 'Mexican',
            'Pasta': 'Italian',
            'Curry': 'Indian',
            'BBQ': 'Barbecue',
            'Dim Sum': 'Chinese',
            'Kebab': 'Middle Eastern'
        }

        for keyword, cuisine in cuisine_keywords.items():
            if keyword.lower() in name.lower():
                return cuisine
        return 'Unknown'
