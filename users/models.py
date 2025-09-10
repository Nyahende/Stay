from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ("guest", "Guest"),
        ("owner", "Owner"),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="guest")

    def __str__(self):
        return self.username
