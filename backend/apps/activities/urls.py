from django.urls import path
from .views import activity_list, activity_detail

urlpatterns = [
    path("", activity_list, name="activity-list"),
    path("<uuid:pk>/", activity_detail, name="activity-detail"),
]
