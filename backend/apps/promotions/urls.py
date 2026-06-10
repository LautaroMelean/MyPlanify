from django.urls import path
from .views import promotion_list, promotion_detail, promotion_activate, promotion_cancel

urlpatterns = [
    path("", promotion_list, name="promotion-list"),
    path("<uuid:pk>/", promotion_detail, name="promotion-detail"),
    path("<uuid:pk>/activate/", promotion_activate, name="promotion-activate"),
    path("<uuid:pk>/cancel/", promotion_cancel, name="promotion-cancel"),
]
