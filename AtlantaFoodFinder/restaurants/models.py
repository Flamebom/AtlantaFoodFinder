from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=255)
    location = models.CharField(max_length=255)  # Could be an address or a city name
    latitude = models.FloatField()  # Latitude of the restaurant
    longitude = models.FloatField()  # Longitude of the restaurant
    rating = models.FloatField()  # Rating out of 5
    distance = models.FloatField()  # Distance in kilometers (if you're calculating this)

    def __str__(self):
        return self.name
