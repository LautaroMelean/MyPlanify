from rest_framework import serializers
from .models import Place


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = (
            "id", "name", "description", "category", "address", "city",
            "latitude", "longitude", "phone", "website", "image_url",
            "price_level", "is_active", "source", "external_id", "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class PlaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = (
            "name", "description", "category", "address", "city",
            "latitude", "longitude", "phone", "website", "image_url", "price_level",
        )
