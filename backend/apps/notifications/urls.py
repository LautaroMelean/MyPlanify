from django.urls import path
from .views import notification_list, notification_read, notification_mark_all_read, reminder_list, reminder_detail

urlpatterns = [
    path("", notification_list, name="notification-list"),
    path("read-all/", notification_mark_all_read, name="notification-read-all"),
    path("<uuid:pk>/read/", notification_read, name="notification-read"),
    path("reminders/", reminder_list, name="reminder-list"),
    path("reminders/<uuid:pk>/", reminder_detail, name="reminder-detail"),
]
