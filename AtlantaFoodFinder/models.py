from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.conf import settings  # Import settings to reference AUTH_USER_MODEL

# Extends existing user model to add new fields for favorites specifically associated to the account
class CustomUser(AbstractUser):
    favorite_restaurant = models.CharField(max_length=255, blank=True, null=True)
    # creates table for favorite_restaurants associated with "CustomUser" object

    def add_favorite(self, restaurant_name, restaurant_address):
        favorite, created = Favorite.objects.get_or_create(
            user=self,
            restaurant_name=restaurant_name,
            defaults={'restaurant_address': restaurant_address}
        )
        if created:
            return favorite, "Favorite added"
        return favorite, "Already favorited"

    def remove_favorite(self, restaurant_name):
        try:
            favorite = Favorite.objects.get(user=self, restaurant_name=restaurant_name)
            favorite.delete()
            return "Favorite removed"
        except Favorite.DoesNotExist:
            return "Favorite not found"

    def get_favorites(self):
        return Favorite.objects.filter(user=self)

class Favorite(models.Model):
    # Reference the CustomUser model
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=255)
    restaurant_address = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant_name')

    def __str__(self):
        return f"{self.user.username} favorited {self.restaurant_name}"
