# urls.py

from django.urls import path
from .views import (
    signup,
    CustomLoginView,
    favorite_list,
    favorite_restaurant,
    remove_favorite_restaurant,
    ResetPasswordView,
    home_view,
)

urlpatterns = [
    path('', home_view, name='index'),
    path('login/create-account.html', signup, name='create-account'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('favorites/', favorite_list, name='favorite_list'),
    path('favorites/add/<str:restaurant_name>/<str:restaurant_address>/', favorite_restaurant, name='favorite_restaurant'),
    path('favorites/remove/<str:restaurant_name>/', remove_favorite_restaurant, name='remove_favorite_restaurant'),
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
]
