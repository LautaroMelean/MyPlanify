from django.urls import path, include

urlpatterns = [
    path("health/", include("apps.core.urls")),
    path("auth/", include("apps.users.urls.auth")),
    path("users/", include("apps.users.urls.users")),
    path("preferences/", include("apps.users.urls.preferences")),
    path("places/", include("apps.places.urls")),
    path("events/", include("apps.events.urls")),
    path("activities/", include("apps.activities.urls")),
    path("recommendations/", include("apps.recommendations.urls")),
    path("favorites/", include("apps.favorites.urls")),
    path("promotions/", include("apps.promotions.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("reminders/", include("apps.notifications.reminder_urls")),
]
