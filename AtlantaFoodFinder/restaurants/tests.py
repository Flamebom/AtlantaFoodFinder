from django.test import TestCase
from .models import Restaurant

class RestaurantSearchTestCase(TestCase):
    def setUp(self):
        Restaurant.objects.create(name="Pizza Palace", cuisine_type="Italian", location="New York", latitude=40.7128, longitude=-74.0060)
        Restaurant.objects.create(name="Sushi Spot", cuisine_type="Japanese", location="San Francisco", latitude=37.7749, longitude=-122.4194)
        Restaurant.objects.create(name="Burger Barn", cuisine_type="American", location="Los Angeles", latitude=34.0522, longitude=-118.2437)

    def test_search_by_name(self):
        response = self.client.get('/restaurants/search/', {'name': 'Pizza Palace'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pizza Palace")
        self.assertNotContains(response, "Sushi Spot")
        self.assertNotContains(response, "Burger Barn")

    def test_search_by_cuisine_type(self):
        response = self.client.get('/restaurants/search/', {'cuisine_type': 'Italian'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pizza Palace")
        self.assertNotContains(response, "Sushi Spot")
        self.assertNotContains(response, "Burger Barn")

    def test_search_by_location(self):
        response = self.client.get('/restaurants/search/', {'location': 'New York'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Pizza Palace")
        self.assertNotContains(response, "Sushi Spot")
        self.assertNotContains(response, "Burger Barn")
