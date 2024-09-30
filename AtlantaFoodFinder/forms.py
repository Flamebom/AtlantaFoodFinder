from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser  # If you are using a custom user model, otherwise import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email_address', 'password1', 'confirmation_password']