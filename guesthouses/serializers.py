from rest_framework import serializers
from .models import GuestHouse, GuestHouseImage

class GuestHouseImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuestHouseImage
        fields = ['image']

class GuestHouseSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    images = serializers.SerializerMethodField()
    amenities = serializers.SerializerMethodField()
    video = serializers.SerializerMethodField()

    class Meta:
        model = GuestHouse
        fields = [
            'id', 'owner', 'owner_username', 'name', 'region', 'city', 'description',
            'price_per_night', 'amenities', 'availability_status', 'max_rooms',
            'rooms_available', 'video', 'images', 'latitude', 'longitude',
            'location_link', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'owner_username', 'created_at', 'updated_at']

    def get_amenities(self, obj):
        return obj.amenities.split(',') if obj.amenities else []

    def get_images(self, obj):
        images = obj.images.all()
        return [image.image.url for image in images]

    def get_video(self, obj):
        return obj.video.url if obj.video else None

    def create(self, validated_data):
        images = self.context['request'].FILES.getlist('images', [])
        video = self.context['request'].FILES.get('video')
        guesthouse = GuestHouse.objects.create(**validated_data)
        if video:
            guesthouse.video = video
            guesthouse.save()
        for image in images:
            GuestHouseImage.objects.create(guesthouse=guesthouse, image=image)
        guesthouse.update_availability_status()
        return guesthouse