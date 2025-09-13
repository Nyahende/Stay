from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

def guesthouse_image_upload_path(instance, filename):
    return f"guesthouses/{instance.guesthouse.id}/images/{filename}"

def guesthouse_video_upload_path(instance, filename):
    return f"guesthouses/{instance.id}/video/{filename}"

class GuestHouse(models.Model):
    AVAILABILITY_CHOICES = [
        ("available", "Available"),
        ("few", "Few Rooms Left"),
        ("full", "Full"),
    ]

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guesthouses"
    )
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=100)          # e.g., Morogoro, Arusha
    city = models.CharField(max_length=100, blank=True)  # optional more granular
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    # Simple CSV storage for amenities (MVP). Frontend/serializers will expose it as list.
    amenities = models.TextField(
        blank=True,
        help_text="Comma-separated amenities, e.g. WiFi,Breakfast,Parking"
    )
    # location fields
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    location_link = models.URLField(blank=True, help_text="Google Maps link (optional)")

    # availability & room counts
    max_rooms = models.PositiveIntegerField(default=1)
    rooms_available = models.IntegerField(default=1)
    availability_status = models.CharField(
        max_length=20,
        choices=AVAILABILITY_CHOICES,
        default="available"
    )

    # Media
    video = models.FileField(
        upload_to=guesthouse_video_upload_path,
        blank=True,
        null=True,
        help_text="Optional short video showcasing the guesthouse"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Guest House"
        verbose_name_plural = "Guest Houses"

    def __str__(self):
        return f"{self.name} — {self.region}"

    def update_availability_status(self):
        """
        Helper to update availability_status based on rooms_available/max_rooms.
        Call this after bookings or when owner updates rooms_available.
        """
        if self.rooms_available <= 0:
            self.availability_status = "full"
        elif 0 < self.rooms_available <= max(1, int(self.max_rooms * 0.25)):
            # When <= 25% rooms left, mark as few
            self.availability_status = "few"
        else:
            self.availability_status = "available"
        self.save()

class GuestHouseImage(models.Model):
    guesthouse = models.ForeignKey(
        GuestHouse,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to=guesthouse_image_upload_path)

    def __str__(self):
        return f"Image for {self.guesthouse.name}"
