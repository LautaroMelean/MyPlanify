from rest_framework import serializers
from apps.core.mixins import RatingMixin
from .models import Event


class EventSerializer(RatingMixin, serializers.ModelSerializer):
    place_name = serializers.CharField(source="place.name", read_only=True, default=None)
    organizer_email = serializers.EmailField(source="organizer.email", read_only=True, default=None)
    avg_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            "id", "title", "description", "category", "start_date", "end_date",
            "minimum_age", "capacity", "price", "image_url", "status",
            "place", "place_name", "organizer_email",
            "avg_rating", "review_count", "created_at", "updated_at",
        )
        read_only_fields = ("id", "status", "organizer_email", "created_at", "updated_at")


class EventCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "place", "title", "description", "category", "start_date", "end_date",
            "minimum_age", "capacity", "price", "image_url",
        )

    def validate(self, attrs):
        if attrs.get("end_date") and attrs.get("start_date"):
            if attrs["end_date"] <= attrs["start_date"]:
                raise serializers.ValidationError({"end_date": "La fecha de fin debe ser posterior a la de inicio."})
        return attrs
