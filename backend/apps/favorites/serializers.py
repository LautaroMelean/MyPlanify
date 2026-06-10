from rest_framework import serializers
from .models import Favorite


class FavoriteSerializer(serializers.ModelSerializer):
    item_type = serializers.SerializerMethodField()
    item_name = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ("id", "event", "place", "activity", "item_type", "item_name", "created_at")
        read_only_fields = ("id", "item_type", "item_name", "created_at")

    def validate(self, attrs):
        refs = [attrs.get("event"), attrs.get("place"), attrs.get("activity")]
        filled = [r for r in refs if r is not None]
        if len(filled) != 1:
            raise serializers.ValidationError("Indicá exactamente uno de: event, place o activity.")
        return attrs

    def get_item_type(self, obj):
        if obj.event_id:
            return "event"
        if obj.place_id:
            return "place"
        if obj.activity_id:
            return "activity"
        return None

    def get_item_name(self, obj):
        if obj.event_id:
            return obj.event.title
        if obj.place_id:
            return obj.place.name
        if obj.activity_id:
            return obj.activity.name
        return None
