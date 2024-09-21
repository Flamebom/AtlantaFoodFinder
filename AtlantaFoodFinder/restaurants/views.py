import json
from django.shortcuts import render
from .models import Restaurant
from .forms import RestaurantSearchForm  # Import the search form if you're using it
from AtlantaFoodFinder import settings

def search_restaurants(request):
    form = RestaurantSearchForm(request.GET or None)
    restaurants = Restaurant.objects.all()

    if form.is_valid():  # Check if form data is valid
        if form.cleaned_data['name']:
            restaurants = restaurants.filter(name__icontains=form.cleaned_data['name'])
        if form.cleaned_data['cuisine_type']:
            restaurants = restaurants.filter(cuisine_type__icontains=form.cleaned_data['cuisine_type'])
        if form.cleaned_data['location']:
            restaurants = restaurants.filter(location__icontains=form.cleaned_data['location'])
        if form.cleaned_data['rating']:
            restaurants = restaurants.filter(rating__gte=form.cleaned_data['rating'])

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
        'form': form,  # Pass the form for search criteria
        'restaurants': restaurants,  # Pass the queryset directly for the template
        'restaurant_data_json': json.dumps(restaurant_data),  # Only if needed for JavaScript
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY  # For embedding Google Maps
    }

    return render(request, 'restaurants/search_results.html', context)
