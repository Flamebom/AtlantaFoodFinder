from django.db import models
from django.contrib.auth.models import User

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=250)  # Identifier for the restaurant name
    restaurant_address = models.CharField(max_length=250)  # Storing essential restaurant info
    date_added = models.DateTimeField(auto_now_add=True)
    #could add more info to the favorite system; not sure if it is neccesary

    class Meta:
        unique_together = ('user', 'restaurant_name')
        #can only favorite a restaurant once per user

    def __str__(self):
        return f"{self.user.username} favorited {self.restaurant_name}"
