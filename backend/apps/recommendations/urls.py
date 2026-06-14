from django.urls import path
from .views import recommendation_list, recommendation_click

urlpatterns = [
    path("", recommendation_list, name="recommendation-list"),
    path("click/", recommendation_click, name="recommendation-click"),
]
