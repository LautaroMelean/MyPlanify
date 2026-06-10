from django.urls import path
from .views import event_list, event_detail, event_publish, event_cancel

urlpatterns = [
    path("", event_list, name="event-list"),
    path("<uuid:pk>/", event_detail, name="event-detail"),
    path("<uuid:pk>/publish/", event_publish, name="event-publish"),
    path("<uuid:pk>/cancel/", event_cancel, name="event-cancel"),
]
