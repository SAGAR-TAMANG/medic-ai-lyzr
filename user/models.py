from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    LANGUAGE_CHOICES = [
        ("en", "English"),
        ("hi", "Hindi"),
        ("bn", "Bengali"),
        ("as", "Assamese"),
    ]
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default="en")

    def __str__(self):
        return self.user.username
