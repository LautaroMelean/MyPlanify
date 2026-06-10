from .models import Notification, Reminder


def get_user_notifications(user):
    return Notification.objects.filter(user=user).order_by("-created_at")


def get_user_reminders(user):
    return Reminder.objects.filter(user=user).select_related("event").order_by("reminder_date")
