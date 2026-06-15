from django.urls import path
from . import views

urlpatterns = [
    path("generate/", views.generate_plan_view, name="plan-generate"),
    path("trending/", views.plan_trending, name="plan-trending"),
    path("surprise/", views.plan_surprise, name="plan-surprise"),
    path("", views.plan_list, name="plan-list"),
    path("<uuid:plan_id>/", views.plan_detail, name="plan-detail"),
    path("<uuid:plan_id>/items/", views.add_plan_item, name="plan-add-item"),
    path("<uuid:plan_id>/items/<uuid:item_id>/", views.plan_item_detail, name="plan-item-detail"),
    path("<uuid:plan_id>/share/", views.plan_share, name="plan-share"),
    path("<uuid:plan_id>/feedback/", views.plan_feedback, name="plan-feedback"),
    path("<uuid:plan_id>/clone/", views.plan_clone, name="plan-clone"),
    path("public/<slug:slug>/", views.public_plan, name="plan-public"),
]
