
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm  # The form we defined earlier
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import views as auth_views
from django.contrib.auth import login
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm  # Import the form
from django.contrib.auth import login

from django.shortcuts import render

def home_view(request):
    return render(request, 'index.html')  # Need to make home.html template
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
            return redirect('home')  # Redirect to homepage or any other page
    else:
        form = CustomUserCreationForm()

    return render(request, 'signup.html', {'form': form})


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

# Custom login view using the built-in LoginView
class CustomLoginView(LoginView):
    template_name = 'login.html'  # Login interface

@login_required
def favorite_restaurant(request, restaurant_name):
    user = request.user  # Get the logged-in user
    favorite, message = user.add_favorite(restaurant_name)
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
