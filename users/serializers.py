from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'required': True},
            'email': {'required': True},
        }

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("Email is required.")
        if '@' not in value or '.' not in value:
            raise serializers.ValidationError("Enter a valid email address.")
        return value

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError("Username is required.")
        if get_user_model().objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password is required.")
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user