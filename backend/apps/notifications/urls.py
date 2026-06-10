from django.urls import path
from .views import notification_list, notification_read, reminder_list, reminder_detail

urlpatterns = [
    path("", notification_list, name="notification-list"),
    path("<uuid:pk>/read/", notification_read, name="notification-read"),
    path("reminders/", reminder_list, name="reminder-list"),
    path("reminders/<uuid:pk>/", reminder_detail, name="reminder-detail"),
]
