from django.contrib import admin
from .models import GuestHouse

@admin.register(GuestHouse)
class GuestHouseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "region", "price_per_night", "availability_status", "rooms_available")
    list_filter = ("region", "availability_status", "created_at")
    search_fields = ("name", "region", "owner__username")
