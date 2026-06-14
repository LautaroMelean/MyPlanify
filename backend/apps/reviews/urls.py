from django.urls import path
from . import views

urlpatterns = [
    path("", views.review_create, name="review-create"),
    path("<str:entity_type>/<uuid:entity_id>/", views.review_list, name="review-list"),
    path("<str:entity_type>/<uuid:entity_id>/delete/", views.review_delete, name="review-delete"),
]
