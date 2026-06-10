from rest_framework import serializers
from .models import Notification, Reminder


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("id", "title", "message", "notification_type", "status", "read", "created_at")
        read_only_fields = fields


class ReminderSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source="event.title", read_only=True)

    class Meta:
        model = Reminder
        fields = ("id", "event", "event_title", "reminder_date", "created_at")
        read_only_fields = ("id", "created_at", "event_title")
