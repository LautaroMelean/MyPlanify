from django.urls import path
from apps.users.views.user_views import (
    user_list,
    user_detail,
    user_preferences,
    user_preference_detail,
    change_password_view,
)

urlpatterns = [
    path("", user_list, name="user-list"),
    path("<uuid:pk>/", user_detail, name="user-detail"),
    path("me/preferences/", user_preferences, name="user-preferences"),
    path("me/preferences/<uuid:pk>/", user_preference_detail, name="user-preference-detail"),
    path("me/change-password/", change_password_view, name="user-change-password"),
]
