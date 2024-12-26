from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
  list_display = ('user', 'language')  # Display these fields in the admin list view

admin.site.register(UserProfile, UserProfileAdmin)
