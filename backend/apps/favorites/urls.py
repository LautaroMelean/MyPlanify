from django.urls import path
from .views import favorite_list, favorite_detail

urlpatterns = [
    path("", favorite_list, name="favorite-list"),
    path("<uuid:pk>/", favorite_detail, name="favorite-detail"),
]
