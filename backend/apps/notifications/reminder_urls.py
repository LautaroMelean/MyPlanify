from django.urls import path
from .views import reminder_list, reminder_detail

urlpatterns = [
    path("", reminder_list, name="reminder-list-v2"),
    path("<uuid:pk>/", reminder_detail, name="reminder-detail-v2"),
]
