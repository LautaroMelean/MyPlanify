from django.urls import path
from .views import place_list, place_detail

urlpatterns = [
    path("", place_list, name="place-list"),
    path("<uuid:pk>/", place_detail, name="place-detail"),
]
