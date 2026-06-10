import uuid
from django.db import models
from django.conf import settings


class NotificationType(models.TextChoices):
    EVENT_REMINDER = "event_reminder", "Event Reminder"
    PROMOTION = "promotion", "Promotion"
    SYSTEM = "system", "System"
    RECOMMENDATION = "recommendation", "Recommendation"


class NotificationStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SENT = "sent", "Sent"
    FAILED = "failed", "Failed"


class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=30, choices=NotificationType.choices)
    status = models.CharField(max_length=20, choices=NotificationStatus.choices, default=NotificationStatus.PENDING)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "notifications"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "read", "-created_at"])]

    def __str__(self):
        return f"{self.user.email} — {self.title}"


class Reminder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reminders")
    event = models.ForeignKey("events.Event", on_delete=models.CASCADE, related_name="reminders")
    reminder_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reminders"
        unique_together = ("user", "event")
        ordering = ["reminder_date"]

    def __str__(self):
        return f"{self.user.email} — reminder for {self.event.title}"
