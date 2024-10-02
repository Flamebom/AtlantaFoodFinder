# urls.py
from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views

from AtlantaFoodFinder import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('favorite/<str:restaurant_name>/<str:restaurant_address>/', views.favorite_restaurant, name='favorite_restaurant'),
    path('remove_favorite/<str:restaurant_name>/', views.remove_favorite_restaurant, name='remove_favorite_restaurant'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('admin/', admin.site.urls),
    path('signup/', views.signup, name='signup'),
    # Login and logout URLs using Django's built-in views
    path('login/', views.login_view, name='login'),
    #login interface
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password-reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),
]
