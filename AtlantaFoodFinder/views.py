from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm  # The form we defined earlier
from django.contrib.auth import views as auth_views


# User registration view
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            login(request, user)  # Automatically log the user in
            return redirect('home')  # Redirect to homepage or another page
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})
    #registration interface is signup.html
def login_view(request):
    return auth_views.LoginView.as_view(template_name='login.html')(request)
    #login.html is the interface for logging in

from django.shortcuts import render, redirect
from .models import CustomUser, Favorite
from django.contrib.auth.decorators import login_required

@login_required
def favorite_restaurant(request, restaurant_name, restaurant_address):
    user = CustomUser.objects.get(pk=request.user.pk)  # Explicitly get CustomUser instance
    favorite, message = user.add_favorite(restaurant_name, restaurant_address)
    return redirect('restaurant_list')

@login_required
def remove_favorite_restaurant(request, restaurant_name):
    user = CustomUser.objects.get(pk=request.user.pk)  # Explicitly get CustomUser instance
    message = user.remove_favorite(restaurant_name)
    return redirect('favorite_list')

@login_required
def favorite_list(request):
    user = CustomUser.objects.get(pk=request.user.pk)  # Explicitly get CustomUser instance
    favorites = user.get_favorites()
    return render(request, 'favorite_list.html', {'favorites': favorites})
    #favorite_list.html is the temp. name for frontend with all the favorites displayed