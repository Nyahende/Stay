# app/serializers.py
from rest_framework import serializers
from .models import GuestHouse, GuestHouseImage, RoomType, RoomTypeImage

class GuestHouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestHouseImage
        fields = ['image']

class RoomTypeImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomTypeImage
        fields = ['image']

class RoomTypeSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()

    class Meta:
        model = RoomType
        fields = ['id', 'name', 'price', 'max_rooms', 'rooms_available', 'amenities', 'images']

    def get_images(self, obj):
        return [img.image.url for img in obj.images.all()]

    def get_amenities(self, obj):
        return obj.amenities.split(',') if obj.amenities else []

class GuestHouseSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    images = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    room_types = RoomTypeSerializer(many=True, read_only=True)

    class Meta:
        model = GuestHouse
        fields = [
            'id', 'owner', 'owner_username', 'name', 'region', 'city', 'description',
            'price_per_night', 'amenities', 'availability_status', 'max_rooms',
            'rooms_available', 'images', 'room_types', 'latitude', 'longitude',
            'location_link', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'owner_username', 'created_at', 'updated_at']

    def get_amenities(self, obj):
        return obj.amenities.split(',') if obj.amenities else []

    def get_images(self, obj):
        return [image.image.url for image in obj.images.all()]

    def create(self, validated_data):
        """
        Handle multipart creation:
        - Guesthouse-level images come as request.FILES.getlist('images')
        - room_types: a JSON array provided in request.data['room_types']
        - for each room type index i, files expected under request.FILES.getlist(f'room_images_{i}')
        """
        request = self.context.get('request')
        # Create guesthouse first
        guesthouse = GuestHouse.objects.create(**validated_data)

        # Guesthouse images (field name: 'images')
        images = request.FILES.getlist('images')
        for image in images:
            GuestHouseImage.objects.create(guesthouse=guesthouse, image=image)

        # Parse room_types JSON (if supplied)
        room_types_raw = request.data.get('room_types')
        if room_types_raw:
            import json
            if isinstance(room_types_raw, str):
                try:
                    room_types_data = json.loads(room_types_raw)
                except Exception:
                    room_types_data = []
            else:
                room_types_data = room_types_raw
        else:
            room_types_data = []

        # room_types_data expected: list of dicts: { "name": "...", "price": 12345, "max_rooms": 10, "amenities": ["WiFi", "Breakfast"] }
        for idx, rt in enumerate(room_types_data):
            name = rt.get('name') or rt.get('type') or ''
            price = rt.get('price') or 0
            max_rooms = rt.get('max_rooms') or rt.get('rooms') or 1
            amenities_list = rt.get('amenities') or rt.get('amenities_list') or []
            amenities_csv = ','.join(amenities_list) if isinstance(amenities_list, (list, tuple)) else (amenities_list or '')

            room_type = RoomType.objects.create(
                guesthouse=guesthouse,
                name=name,
                price=price,
                max_rooms=max_rooms,
                rooms_available=max_rooms,
                amenities=amenities_csv
            )

            # Attach images for this room type: 'room_images_{idx}'.
            room_images = request.FILES.getlist(f'room_images_{idx}')
            for image in room_images:
                RoomTypeImage.objects.create(room_type=room_type, image=image)

        guesthouse.update_availability_status()
        return guesthouse
