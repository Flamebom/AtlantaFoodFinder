from django.urls import path
from . import views  # Import views from the current app

urlpatterns = [
    path('search/', views.search_restaurants, name='search_restaurants'),  # This is the search URL
]
