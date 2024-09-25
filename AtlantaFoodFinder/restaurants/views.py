import json
from django.shortcuts import render
from .models import Restaurant
from .forms import RestaurantSearchForm
from AtlantaFoodFinder import settings
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance
def search_restaurants(request):
    form = RestaurantSearchForm(request.GET or None)
    user_latitude = request.GET.get('latitude')
    user_longitude = request.GET.get('longitude')

    restaurants = Restaurant.objects.all()

    if form.is_valid():
        if form.cleaned_data['name']:
            restaurants = restaurants.filter(name__icontains=form.cleaned_data['name'])
        if form.cleaned_data['cuisine_type']:
            restaurants = restaurants.filter(cuisine_type__icontains=form.cleaned_data['cuisine_type'])
        if form.cleaned_data['location']:
            restaurants = restaurants.filter(location__icontains=form.cleaned_data['location'])
        if form.cleaned_data['rating']:
            restaurants = restaurants.filter(rating__gte=form.cleaned_data['rating'])


    for restaurant in restaurants:
        restaurant.distance = haversine_distance(
            float(user_latitude), float(user_longitude),
            restaurant.latitude, restaurant.longitude
        )

    restaurants = sorted(restaurants, key=lambda x: (x.distance, -x.rating))

    # Need JSON for JavaScript:
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
        'form': form,
        'restaurants': restaurants,
        'restaurant_data_json': json.dumps(restaurant_data),
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }

    return render(request, 'restaurants/search_results.html', context)
