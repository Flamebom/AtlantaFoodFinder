from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Favorite
from django.core import mail

# Import CustomUser model dynamically using get_user_model()
CustomUser = get_user_model()
from django.core.mail import send_mail

send_mail(
    'Test Subject',
    'Test message body.',
    'atlantarestaurantfinder@gmail.com',  # From email
    ['testuser@example.com'],  # To email
    fail_silently=True,
)
class CustomUserTestCase(TestCase):
    def setUp(self):
        # Create a sample user using CustomUser model
        self.user = CustomUser.objects.create_user(
            email='testuser@example.com',
            password='testpassword123'
        )
        # Log the user in
        self.client.login(email='testuser@example.com', password='testpassword123')

    def test_login(self):
        # Test logging in the user
        login_successful = self.client.login(email='testuser@example.com', password='testpassword123')
        self.assertTrue(login_successful)

    def test_signup(self):
        # Test signing up a new user
        response = self.client.post(reverse('signup'), {
            'email': 'newuser@example.com',
            'password1': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Assuming successful signup redirects
        self.assertTrue(CustomUser.objects.filter(email='newuser@example.com').exists())

    def test_add_favorite_restaurant(self):
        restaurant_name = 'Pizza Place'

        # Add a favorite restaurant
        favorite, message = self.user.add_favorite(restaurant_name)

        # Check if the favorite was created
        self.assertEqual(message, "Favorite added")
        self.assertEqual(favorite.restaurant_name, restaurant_name)
        self.assertEqual(favorite.user, self.user)

    def test_add_duplicate_favorite_restaurant(self):
        restaurant_name = 'Pizza Place'

        # Add the restaurant for the first time
        self.user.add_favorite(restaurant_name)

        # Try adding the same restaurant again
        favorite, message = self.user.add_favorite(restaurant_name)

        # Check that it was not added again
        self.assertEqual(message, "Already favorited")
        self.assertEqual(Favorite.objects.count(), 1)  # Should still be only one favorite

    def test_remove_favorite_restaurant(self):
        restaurant_name = 'Pizza Place'
        self.user.add_favorite(restaurant_name)  # Add the restaurant first

        # Now remove the favorite
        message = self.user.remove_favorite(restaurant_name)

        # Verify that it was removed
        self.assertEqual(message, "Favorite removed")
        self.assertEqual(Favorite.objects.count(), 0)  # Should be no favorites left

    def test_remove_nonexistent_favorite_restaurant(self):
        restaurant_name = 'Pizza Place'

        # Attempt to remove a restaurant that doesn't exist
        message = self.user.remove_favorite(restaurant_name)

        # Verify the appropriate message is returned
        self.assertEqual(message, "Favorite not found")

    def test_password_reset_email_sent(self):
        # Request a password reset for the correct email
        response = self.client.post(reverse('password_reset'), {'email': 'testuser@example.com'})

        # Check if an email has been sent
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after form submission
        self.assertEqual(len(mail.outbox), 1)  # One email should be sent
        self.assertIn('testuser@example.com', mail.outbox[0].to)  # The email should be sent to the correct address

    def test_password_reset_email_not_sent_for_invalid_user(self):
        # Request a password reset for an email that doesn't exist
        response = self.client.post(reverse('password_reset'), {'email': 'invalid@example.com'})

        # Check that no email was sent
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after form submission
        self.assertEqual(len(mail.outbox), 0)  # No email should be sent for an invalid email
