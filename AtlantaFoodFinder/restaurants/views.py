import json
from django.shortcuts import render
from .models import Restaurant

def search_restaurants(request):
    restaurants = Restaurant.objects.all()

    restaurant_data = [
        {
            "name": restaurant.name,
            "cuisine_type": restaurant.cuisine_type,
            "location": restaurant.location,
            "latitude": restaurant.latitude,
            "longitude": restaurant.longitude,
            "rating": restaurant.rating,
            "distance": restaurant.distance
        } for restaurant in restaurants
    ]

    context = {
        'restaurants': json.dumps(restaurant_data),  # Pass as JSON string
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
    return render(request, 'restaurants/search_results.html', context)
