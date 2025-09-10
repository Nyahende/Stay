from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    guest = serializers.StringRelatedField(read_only=True)
    guesthouse_name = serializers.ReadOnlyField(source="guesthouse.name")

    class Meta:
        model = Booking
        fields = "__all__"
        read_only_fields = ["guest", "status", "created_at"]
