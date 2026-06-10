from django.urls import path
from .views import recommendation_list

urlpatterns = [
    path("", recommendation_list, name="recommendation-list"),
]
