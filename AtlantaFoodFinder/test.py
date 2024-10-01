from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

# Import CustomUser model dynamically using get_user_model()
CustomUser = get_user_model()

class CustomUserTestCase(TestCase):
    def setUp(self):
        # Create a sample user using CustomUser model
        self.user = CustomUser.objects.create_user(
            username='testuser',
            password='testpassword123',
            email='testuser@example.com'
        )

    def test_login(self):
        # Test logging in the user
        login_successful = self.client.login(username='testuser', password='testpassword123')
        self.assertTrue(login_successful)

    def test_signup(self):
        # Test signing up a new userf
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 302)  # Assuming successful signup redirects
        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())

    def test_favorite_restaurant(self):
        # Test adding a restaurant to the user's favorites
        response = self.client.post(reverse('favorite_restaurant'), {
            'restaurant_name': 'Pizza Place',
            'restaurant_address': '123 Main St'
        })
        self.assertEqual(response.status_code, 302)  # Assuming successful favorite redirects
        self.assertTrue(self.user.favorite_set.filter(restaurant_name='Pizza Place').exists())
