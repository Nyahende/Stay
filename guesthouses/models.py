from django.db import models
from users.models import User

class GuestHouse(models.Model):
    AVAILABILITY_CHOICES = [
        ("available", "Available"),
        ("few", "Few Rooms Left"),
        ("full", "Full"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="guesthouses")
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    amenities = models.TextField(help_text="Comma separated, e.g. WiFi,Breakfast")
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default="available")
    location_link = models.URLField(help_text="Google Maps link", blank=True)

    def __str__(self):
        return f"{self.name} ({self.region})"
