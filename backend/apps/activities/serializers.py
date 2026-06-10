from rest_framework import serializers
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):
    place_name = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = (
            "id", "name", "description", "category", "activity_type",
            "min_budget", "max_budget", "min_people", "max_people",
            "indoor", "outdoor", "score_base", "is_active", "place", "place_name",
            "created_at", "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")

    def get_place_name(self, obj):
        return obj.place.name if obj.place else None


class ActivityCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = (
            "name", "description", "category", "activity_type",
            "min_budget", "max_budget", "min_people", "max_people",
            "indoor", "outdoor", "score_base", "place",
        )
