from rest_framework import serializers
from apps.core.mixins import RatingMixin
from .models import Place
from .utils import OpeningHoursParser


class PlaceSerializer(RatingMixin, serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    is_open_now = serializers.SerializerMethodField()

    class Meta:
        model = Place
        fields = (
            "id", "name", "description", "category", "address", "city",
            "latitude", "longitude", "phone", "website", "image_url",
            "price_level", "is_active", "source", "external_id",
            "opening_hours", "cuisine", "fee", "outdoor_seating",
            "wheelchair", "internet_access", "is_open_now",
            "avg_rating", "review_count", "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def get_is_open_now(self, obj) -> bool | None:
        if not obj.opening_hours:
            return None
        return OpeningHoursParser.is_open(obj.opening_hours)


class PlaceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        fields = (
            "name", "description", "category", "address", "city",
            "latitude", "longitude", "phone", "website", "image_url", "price_level",
        )
