
"""
Class Restaurant contains all the information required for this project, names are self explanatory.
"""
class Restaurant:
    def __init__(self, restaurant_dictionary):
        #print(restaurant_dictionary)
        self.phone_number =restaurant_dictionary.get('nationalPhoneNumber',None)
        self.address = restaurant_dictionary.get('formattedAddress',None)
        self.latitude = restaurant_dictionary['location']['latitude']
        self.longitude = restaurant_dictionary['location']['longitude']
        self.rating = restaurant_dictionary.get('rating',None)
        self.website_url = restaurant_dictionary.get('websiteUri',None)
        self.name = restaurant_dictionary['displayName']['text']
        self.cuisine = restaurant_dictionary['primaryType']
        self.reviews = restaurant_dictionary['reviews']
    def __str__(self):
        return f"name : {self.name} \n cuisine : {self.cuisine}\n phone number : + {self.phone_number} \n address : + {self.address} \n latitude : {self.latitude} \n longitude : {self.longitude} \n rating : {self.rating} \n website_url : {self.website_url} \n reviews : {self.reviews}"