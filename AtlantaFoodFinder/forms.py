from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser  # Import your custom user model

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email_address', 'password1', 'password2']  # Use your custom fields

    def clean_email_address(self):
        email = self.cleaned_data.get('email_address')
        if CustomUser.objects.filter(email_address=email).exists():
            raise forms.ValidationError("Email already exists.")
        return email
