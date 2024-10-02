from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm  # The form we defined earlier
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.shortcuts import render, redirect
from .models import CustomUser, Favorite
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect


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

# Use Django's LoginView
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Redirect to homepage or any other page
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password_reset.html' #html page for resetting password
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')
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