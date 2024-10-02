from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Favorite

# Import CustomUser model dynamically using get_user_model()
CustomUser = get_user_model()

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

    def test_favorite_restaurant(self):
        # Define the restaurant data
        restaurant_name = 'Pizza Place'

        # Reverse the URL and ensure to pass restaurant_name and restaurant_address as arguments
        url = reverse('favorite_restaurant', args=[restaurant_name])

        # Perform the POST request to favorite the restaurant
        response = self.client.post(url)

        # Assert that the response status code is 302 (for a redirect after adding to favorites)
        self.assertEqual(response.status_code, 302)

        # Verify that the restaurant was added to the user's favorites
        self.assertTrue(Favorite.objects.filter(user=self.user, restaurant_name=restaurant_name).exists())

    def test_remove_favorite_restaurant(self):
        # Add a favorite restaurant first
        restaurant_name = 'Burger Joint'
        Favorite.objects.create(user=self.user, restaurant_name=restaurant_name)

        # Reverse the URL for removing the favorite
        url = reverse('remove_favorite_restaurant', args=[restaurant_name])

        # Perform the POST request to remove the restaurant from favorites
        response = self.client.post(url)

        # Assert that the response status code is 302 (for a redirect after removing from favorites)
        self.assertEqual(response.status_code, 302)

        # Verify that the restaurant was removed from the user's favorites
        self.assertFalse(Favorite.objects.filter(user=self.user, restaurant_name=restaurant_name).exists())

    def test_favorite_list(self):
        # Add a favorite restaurant first
        restaurant_name = 'Taco Palace'
        restaurant_address = '789 Taco Rd'
        Favorite.objects.create(user=self.user, restaurant_name=restaurant_name, restaurant_address=restaurant_address)

        # Reverse the URL for the favorite list
        url = reverse('favorite_list')

        # Perform the GET request to retrieve the favorite list
        response = self.client.get(url)

        # Assert that the response status code is 200 (for a successful page load)
        self.assertEqual(response.status_code, 200)

        # Verify that the favorite restaurant is included in the context
        self.assertContains(response, restaurant_name)
        self.assertContains(response, restaurant_address)

    def test_signup_invalid_email(self):
        # Test signing up with an invalid email
        response = self.client.post(reverse('signup'), {
            'email': 'invalid-email',
            'password1': 'newpassword123'
        })
        self.assertEqual(response.status_code, 200)  # Assuming it re-renders the signup page
        self.assertFalse(CustomUser.objects.filter(email='invalid-email').exists())
