from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    cuisine_type = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(null=False)
    longitude = models.FloatField(null=False)
    rating = models.FloatField(null=True, blank=True)
    distance = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name
