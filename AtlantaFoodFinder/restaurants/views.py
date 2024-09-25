import json
from django.shortcuts import render
from .models import Restaurant
from .forms import RestaurantSearchForm

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
        'restaurants': restaurants,  # this is filtered results
    }
    return render(request, 'restaurants/search_results.html', context)
