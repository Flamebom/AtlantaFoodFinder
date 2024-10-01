from django.contrib.auth.models import User, AbstractUser
from django.db import models
from django.conf import settings  # Import settings to reference AUTH_USER_MODEL

# Extends existing user model to add new fields for favorites specifically associated to the account
class CustomUser(AbstractUser):
    email_address = models.EmailField(unique=True, blank=False, null=False)
    password = models.CharField(max_length=128, blank=False, null=False)
    favorite_restaurant = models.CharField(max_length=255, blank=True, null=True)
    # creates table for favorite_restaurants associated with "CustomUser" object
    def reset_password(self):
        pass
    def add_favorite(self, restaurant_name, restaurant_address, cuisine):
        favorite, created = Favorite.objects.get_or_create(
            user=self,
            restaurant_name=restaurant_name,
            cuisine=cuisine,
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
    # Reference the CustomUser model via AUTH_USER_MODEL
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=255)
    restaurant_address = models.CharField(max_length=255)
    cuisine = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant_name')

    def __str__(self):
        return f"{self.user.email_address} favorited {self.restaurant_name}"
