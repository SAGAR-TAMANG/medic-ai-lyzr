from django.contrib import admin
from django.urls import path, include
from .views import account, login, signup, verification_sent, profile, logout

urlpatterns = [
  # path('profile/', profile, name='profile'),
  
  # path('loginn/', login, name='login'),
  # path('signupp/', signup, name='signup'),
  
  # path('confirm-email/', verification_sent, name='verification_sent'),
  # path('logout/', logout, name='logout'),
  # path('', account, name='account'),
  # path('', include('allauth.urls')),
]