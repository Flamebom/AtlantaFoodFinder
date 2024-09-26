import math
"""
Class Restaurant contains all the information required for this project, names are self explanatory.
"""
class Restaurant:
    def __init__(self, restaurant_dictionary,user_latitude, user_longitude):
        #print(restaurant_dictionary)
        self.phone_number =restaurant_dictionary['nationalPhoneNumber']
        self.address = restaurant_dictionary['formattedAddress']
        self.latitude = restaurant_dictionary['location']['latitude']
        self.longitude = restaurant_dictionary['location']['longitude']
        self.rating = restaurant_dictionary['rating']
        self.website_url = restaurant_dictionary['websiteUri']
        self.name = restaurant_dictionary['displayName']['text']
        self.cuisine = restaurant_dictionary['primaryType']
        self.reviews = restaurant_dictionary['reviews']
        self.distance = self.calculate_distance(user_latitude, user_longitude)


    def calculate_distance(self, user_latitude, user_longitude):
        #Haversine formula
        R = 6371.0
        lat1_rad = math.radians(user_latitude)
        lon1_rad = math.radians(user_longitude)
        lat2_rad = math.radians(self.latitude)
        lon2_rad = math.radians(self.longitude)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c
        return distance

    def __str__(self):
        return f"name : {self.name} \n cuisine : {self.cuisine}\n phone number : + {self.phone_number} \n address : + {self.address} \n latitude : {self.latitude} \n longitude : {self.longitude} \n rating : {self.rating} \n website_url : {self.website_url} \n reviews : {self.reviews}"