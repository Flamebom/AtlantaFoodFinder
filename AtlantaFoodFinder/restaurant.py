class Restaurant:
    def __init__(self, name, rating, address, latitude, longitude, cuisine, phone=None, opening_hours=None, menu=None, website=None, gmaps_client=None):
        self.name = name
        self.rating = rating
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.cuisine = cuisine
        self.phone = phone
        self.opening_hours = opening_hours
        self.menu = menu
        self.website = website
        self.gmaps_client = gmaps_client

    def __repr__(self):
        return f"{self.name} ({self.rating}) - {self.address} [Cuisine: {self.cuisine}, Lat: {self.latitude}, Lng: {self.longitude}]"

    def get_distance(self, current_location, mode='walking'):
        if self.gmaps_client is None:
            raise ValueError("Google Maps client not provided for distance calculations.")

        try:
            result = self.gmaps_client.distance_matrix(
                origins=[current_location],
                destinations=[(self.latitude, self.longitude)],
                mode=mode
            )
            distance_info = result['rows'][0]['elements'][0]
            distance = distance_info['distance']['text']
            duration = distance_info['duration']['text']
            return {
                'distance': distance,
                'duration': duration,
                'mode': mode
            }
        except googlemaps.exceptions.ApiError as e:
            print(f"Error calculating distance: {e}")
            return None
