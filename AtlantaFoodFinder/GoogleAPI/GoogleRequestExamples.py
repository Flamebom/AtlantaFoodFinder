import GoogleRequest
#gets restaurants
output0 = GoogleRequest.get_google_restaurants(33.77865611574625, -84.40530193992045,"Starbucks")
output1 = GoogleRequest.get_google_restaurants(33.77865611574625, -84.40530193992045,)
print(output0[0])
print(output1[1])