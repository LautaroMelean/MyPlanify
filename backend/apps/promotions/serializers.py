from rest_framework import serializers
from .models import Promotion


class PromotionSerializer(serializers.ModelSerializer):
    place_name = serializers.CharField(source="place.name", read_only=True)
    is_currently_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Promotion
        fields = (
            "id", "place", "place_name", "title", "description",
            "discount_percentage", "start_date", "end_date", "status",
            "is_currently_active", "created_at", "updated_at",
        )
        read_only_fields = ("id", "status", "created_at", "updated_at")


class PromotionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ("place", "title", "description", "discount_percentage", "start_date", "end_date")

    def validate_discount_percentage(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("El descuento debe estar entre 0 y 100.")
        return value

    def validate(self, attrs):
        start = attrs.get("start_date")
        end = attrs.get("end_date")
        if start and end and end <= start:
            raise serializers.ValidationError({"end_date": "La fecha de fin debe ser posterior a la de inicio."})
        return attrs
