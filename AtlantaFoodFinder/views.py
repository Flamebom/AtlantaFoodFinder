from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from . import settings
from .models import CustomUser
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView, PasswordResetView
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.urls import reverse_lazy

def home_view(request):
    return render(request, 'index.html')  # Need to make home.html template
# User registration view
def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False
    

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .models import CustomUser
from .forms import CustomUserCreationForm
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')

        # Print received POST data
        print(f"Received POST request with email: {email}")

        # Validate email and password
        if email and password1 and is_valid_email(email):
            print(f"Email {email} is valid and password is provided.")

            # Check if the user already exists
            if CustomUser.objects.filter(email=email).exists():
                print(f"Email {email} already exists.")
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'error': 'Email already exists.'}, status=400)
            else:
                # Create a new user
                user = CustomUser(email=email)
                user.set_password(password1)
                user.save()
                print(f"Created new user with email: {email}")

                # Log in the user
                login(request, user)
                print(f"Logged in user: {email}")

                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True})
                else:
                    return redirect('/index')
        else:
            print("Invalid email or password")

            # If this is an AJAX request, return JSON error
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Invalid email or password.'}, status=400)

        # Initialize form in case of POST request failure
        print("Form initialization after POST request failure")
        form = CustomUserCreationForm()
    else:
        # Initialize form for GET request
        print("Form initialization for GET request")
        form = CustomUserCreationForm()

    # Always render the form (for both GET and POST)
    print("Rendering signup form")
    return render(request, 'signup.html', {'form': form})


from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import JsonResponse
from django.shortcuts import redirect, render
from .forms import EmailAuthenticationForm  # Import the custom form
def login_view(request):
    if request.method == 'POST':
        print("Received POST request for login.")
        form = EmailAuthenticationForm(request, data=request.POST)

        # Check if the form is valid
        if form.is_valid():
            print("Login form is valid.")
            user = form.get_user()

            # Log the user's information
            print(f"Logging in user: {user.email}")
            login(request, user)

            # Check if the request is AJAX
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                print("AJAX request detected, sending JSON success response.")
                return JsonResponse({'success': True})
            else:
                print("Non-AJAX request, redirecting to home.")
                return redirect('index/')
        else:
            print("Login form is invalid.")
            # Log form errors to see why validation failed
            print(f"Form errors: {form.errors}")

            # Handle AJAX request with JSON response if the form is invalid
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = form.errors.get_json_data()
                print(f"Sending JSON response with errors: {errors}")
                return JsonResponse({'success': False, 'error': errors}, status=400)
    else:
        print("Rendering login form (GET request).")
        form = EmailAuthenticationForm()  # Use custom form

    print("Rendering login template with form.")
    return render(request, 'login.html', {'form': form})


class ResetPasswordView(PasswordResetView):
    template_name = 'passwordreset.html'  # Your template for the password reset form
    email_template_name = 'password_reset_email.html'  # Your email template
    subject_template_name = 'password_reset_subject.txt'  # Your email subject template
    success_url = reverse_lazy('index')  # Redirect after sending email

    def form_valid(self, form):
        email = form.cleaned_data['email']
        user = CustomUser.objects.filter(email=email).first()

        if user:
            # Generate the password reset token and uid
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Build the reset link
            reset_link = self.request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            # Send the password reset email
            send_mail(
                subject='Password Reset Request',
                message=f'You requested a password reset. Click the link below to reset your password:\n\n{reset_link}',
                from_email='atlantafoodfinder@gmail.com',  # Replace with your default email
                recipient_list=[email],
                fail_silently=False,
            )

        # Call the parent form_valid to handle the rest
        return super().form_valid(form)
# Custom login view using the built-in LoginView
class CustomLoginView(LoginView):
    template_name = 'login.html'  # Login interface

@login_required
def index(request):
    return render(request, 'index.html')

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def favorite_restaurant(request, restaurant_name):
    user = request.user  # Get the logged-in user
    favorite, created = user.add_favorite(restaurant_name)  # Assuming user model has this method
    if created:
        return JsonResponse({"message": "Restaurant added to favorites"}, status=201)
    else:
        return JsonResponse({"message": "Restaurant already in favorites"}, status=200)

@login_required
def remove_favorite_restaurant(request, restaurant_name):
    user = request.user  # Get the logged-in user
    success = user.remove_favorite(restaurant_name)  # Assuming user model has this method
    if success:
        return JsonResponse({"message": "Restaurant removed from favorites"}, status=200)
    else:
        return JsonResponse({"message": "Restaurant not in favorites"}, status=404)


from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def favorite_list(request):
    user = request.user  # Get the logged-in user
    favorites = user.get_favorites()  # Assuming this returns a list of favorites
    favorite_list = [str(favorite) for favorite in favorites]  # Convert to strings if needed
    return JsonResponse({'favorites': favorite_list})  # Return as JSON


