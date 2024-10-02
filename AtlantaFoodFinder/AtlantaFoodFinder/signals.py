from .models import Favorite

def remove_favorites_with_user(sender, instance, **kwargs):
    # Delete all favorites associated with the user
    Favorite.objects.filter(user=instance).delete()