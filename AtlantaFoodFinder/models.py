from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Set hashed password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No username required

    def add_favorite(self, restaurant_name):
        favorite, created = Favorite.objects.get_or_create(
            user=self,
            restaurant_name=restaurant_name,
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=255)  # Only this field is present
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'restaurant_name')  # Ensures no duplicates per user

    def __str__(self):
        return f"{self.user.email} favorited {self.restaurant_name}"
