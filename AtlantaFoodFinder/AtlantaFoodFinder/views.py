from django.contrib.auth import login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render

def home_view(request):
    return render(request, 'home.html')  # Need to make home.html template
# User registration view
def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')

        if email and password1 and is_valid_email(email):
            user = CustomUser(email=email)
            user.set_password(password1)  # Set hashed password
            user.save()  # Save the user
            login(request, user)  # Automatically log the user in
            return redirect('home')  # Redirect to homepage or another page
    return render(request, 'create-account.html')  # Re-render the form for GET or invalid input

# Custom login view using the built-in LoginView
class CustomLoginView(LoginView):
    template_name = 'login.html'  # Login interface

@login_required
def favorite_restaurant(request, restaurant_name, restaurant_address):
    user = request.user  # Get the logged-in user
    favorite, message = user.add_favorite(restaurant_name, restaurant_address)
    return redirect('favorite_list')

@login_required
def remove_favorite_restaurant(request, restaurant_name):
    user = request.user  # Get the logged-in user
    message = user.remove_favorite(restaurant_name)
    return redirect('favorite_list')

@login_required
def favorite_list(request):
    user = request.user  # Get the logged-in user
    favorites = user.get_favorites()
    return render(request, 'favorite_list.html', {'favorites': favorites})

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'passwordreset.html'  # HTML page for resetting password
    email_template_name = 'password_reset_email.html'
    subject_template_name = 'password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('users-home')
