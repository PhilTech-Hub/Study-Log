"""Defines URL patterns for users"""

from django.urls import path, include
from django.views.generic import TemplateView
from . import views
from django.contrib.auth import views as auth_views


app_name = "users"
urlpatterns = [
    # Include default auth urls.
    path("", include("django.contrib.auth.urls")),
    
    # To log out functionality …,
    path(
        'do-logout/',
        TemplateView.as_view(template_name='base.html'),
        name='do-logout',
    ),
    # Registration page.
    path('register/', views.register, name='register'),
    # Add the login URL pattern
    path('login/', auth_views.LoginView.as_view(), name='login'),  # Add the login URL pattern
    
]
