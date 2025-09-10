from rest_framework import serializers
from .models import GuestHouse

class GuestHouseSerializer(serializers.ModelSerializer):
    availability_flag = serializers.SerializerMethodField()

    class Meta:
        model = GuestHouse
        fields = "__all__"
        read_only_fields = ["owner"]

    def get_availability_flag(self, obj):
        """
        Returns a user-friendly label or status for availability
        """
        if obj.availability_status == "available":
            return "Available"
        elif obj.availability_status == "few":
            return "Few Rooms Left"
        elif obj.availability_status == "full":
            return "Full"
        return "Unknown"
