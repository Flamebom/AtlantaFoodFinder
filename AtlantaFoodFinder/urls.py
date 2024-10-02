# myproject/urls.py
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('favorite/<str:restaurant_name>/', views.favorite_restaurant, name='favorite_restaurant'),
    path('remove_favorite/<str:restaurant_name>/', views.remove_favorite_restaurant, name='remove_favorite_restaurant'),
    path('favorites/', views.favorite_list, name='favorite_list'),
    path('favorites.html/', views.favorite_list, name='favorite_list'),

    path('index.html/', views.index, name='index'),
    path('admin/', admin.site.urls),
    path('create-account.html/', views.signup, name='signup'),
    path('create-account/', views.signup, name='signup'),

    # Login and logout URLs using Django's built-in views
    path('login', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('', auth_views.LoginView.as_view(template_name='login.html'), name='login'),

    #login interface
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('logout.html/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_reset/', views.ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset.html/', views.ResetPasswordView.as_view(), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='login.html'),
         name='password_reset_done'),  # Adjust template name if needed
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='login.html'),
         name='password_reset_confirm'),  # Confirm reset link
    path('password-reset-complete.html/',
         auth_views.PasswordResetCompleteView.as_view(template_name='login.html'),
         name='password_reset_complete'),
]
