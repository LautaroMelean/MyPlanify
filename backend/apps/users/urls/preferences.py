from django.urls import path
from apps.users.views.user_views import user_preferences, user_preference_detail

urlpatterns = [
    path("", user_preferences, name="preference-list"),
    path("<uuid:pk>/", user_preference_detail, name="preference-detail"),
]
