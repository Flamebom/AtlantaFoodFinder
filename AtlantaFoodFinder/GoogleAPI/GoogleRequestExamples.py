import GoogleRequest
#gets restaurants
outputlist = GoogleRequest.get_google_restaurants(45.55860601168696, -122.86519658540723)
#Allows for the print of any attribute, ordered in a list.
#all information in string format of second restaurant
print("all information in string format of third restaurant")
print(outputlist[2])
#name of first restaurant
print("name of first restaurant")
print(outputlist[0].name)
#rating of fourth restaurant
print("rating of fourth restaurant")
print(outputlist[3].rating)
