from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.core.responses import success_response, created_response, no_content_response, error_response
from .serializers import NotificationSerializer, ReminderSerializer
from .selectors import get_user_notifications, get_user_reminders
from .services import create_reminder, delete_reminder, mark_notification_read, mark_all_notifications_read
from .models import Notification, Reminder


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def notification_list(request):
    notifications = get_user_notifications(request.user)
    return success_response(NotificationSerializer(notifications, many=True).data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def notification_read(request, pk):
    try:
        notif = Notification.objects.get(id=pk, user=request.user)
    except Notification.DoesNotExist:
        return error_response("NOT_FOUND", "Notificación no encontrada.", status_code=status.HTTP_404_NOT_FOUND)
    mark_notification_read(notification=notif)
    return success_response(NotificationSerializer(notif).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def notification_mark_all_read(request):
    count = mark_all_notifications_read(user=request.user)
    return success_response({"marked_read": count})


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def reminder_list(request):
    if request.method == "GET":
        reminders = get_user_reminders(request.user)
        return success_response(ReminderSerializer(reminders, many=True).data)

    serializer = ReminderSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    reminder = create_reminder(user=request.user, **serializer.validated_data)
    return created_response(ReminderSerializer(reminder).data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def reminder_detail(request, pk):
    try:
        reminder = Reminder.objects.get(id=pk, user=request.user)
    except Reminder.DoesNotExist:
        return error_response("NOT_FOUND", "Recordatorio no encontrado.", status_code=status.HTTP_404_NOT_FOUND)
    delete_reminder(user=request.user, reminder=reminder)
    return no_content_response()
