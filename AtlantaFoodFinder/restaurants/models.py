from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=255)
    location = models.CharField(max_length=255)  # address or city name
    latitude = models.FloatField()  # Latitude of the rest
    longitude = models.FloatField()  # Longitude of the rest
    rating = models.FloatField()  # Rating out of 5
    distance = models.FloatField()  # Distance

    def __str__(self):
        return self.name
