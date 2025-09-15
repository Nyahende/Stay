# app/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

def guesthouse_image_upload_path(instance, filename):
    # For GuestHouse-level images
    return f"guesthouses/{instance.guesthouse.id}/images/{filename}"

def roomtype_image_upload_path(instance, filename):
    # For RoomType images
    return f"guesthouses/{instance.room_type.guesthouse.id}/roomtypes/{instance.room_type.id}/images/{filename}"

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
    region = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    amenities = models.TextField(
        blank=True,
        help_text="Comma-separated amenities, e.g. WiFi,Breakfast,Parking"
    )
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

    # Media (we will not expose video in serializer per your request)
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
        if self.rooms_available <= 0:
            self.availability_status = "full"
        elif 0 < self.rooms_available <= max(1, int(self.max_rooms * 0.25)):
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

# New model: RoomType
class RoomType(models.Model):
    guesthouse = models.ForeignKey(
        GuestHouse,
        on_delete=models.CASCADE,
        related_name="room_types"
    )
    name = models.CharField(max_length=100)  # e.g., 'A', 'Standard', 'Deluxe'
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[MinValueValidator(0)], default=0)
    max_rooms = models.PositiveIntegerField(default=1)
    rooms_available = models.IntegerField(default=1)
    amenities = models.TextField(
        blank=True,
        help_text="Comma-separated amenities for this room type"
    )

    def __str__(self):
        return f"{self.guesthouse.name} — {self.name}"

# New model: RoomTypeImage
class RoomTypeImage(models.Model):
    room_type = models.ForeignKey(
        RoomType,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to=roomtype_image_upload_path)

    def __str__(self):
        return f"Image for {self.room_type}"
