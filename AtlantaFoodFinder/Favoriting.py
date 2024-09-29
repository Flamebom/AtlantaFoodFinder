from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from .Favorite import Favorite
from django.contrib.auth.decorators import login_required

@login_required
def add_favorite(request):
    if request.method == 'POST':
        restaurant_data = request.POST
        restaurant_name = restaurant_data.get('restaurant_name')
        restaurant_address = restaurant_data.get('restaurant_address')

        # Checks if the restaurant is already favorited; shouldn't be triggered
        # anyway but is just an edge case if frontend allows favoriting
        if Favorite.objects.filter(user=request.user, restaurant_name=restaurant_name).exists():
            return JsonResponse({'message': 'Restaurant already favorited'}, status=400)

        # Create a new favorite
        Favorite.objects.create(user=request.user, restaurant_name=restaurant_name,
                                restaurant_address=restaurant_address)
        return JsonResponse({'message': restaurant_name+ ' has been added to favorites'}, status=201)

@login_required
def remove_favorite(request):
    if request.method == 'POST':
        restaurant_name = request.POST.get('restaurant_name')
        # Remove the favorite
        favorite = get_object_or_404(Favorite, user=request.user, restaurant_name=restaurant_name)
        favorite.delete()
        return JsonResponse({'message': restaurant_name + ' has been removed from favorites'}, status=200)
@login_required
def list_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    favorite_list = [{'restaurant_name': fav.restaurant_name, 'restaurant_address': fav.restaurant_address} for fav in
                     favorites]

    return JsonResponse({'favorites': favorite_list}, status=200)
