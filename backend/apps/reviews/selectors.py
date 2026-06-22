from django.db.models import Avg, Count
from .models import Review


def get_reviews_for_entity(entity_type: str, entity_id):
    return Review.objects.filter(entity_type=entity_type, entity_id=entity_id).select_related("user").order_by("-created_at")[:50]


def get_entity_rating(entity_type: str, entity_id) -> dict:
    result = Review.objects.filter(entity_type=entity_type, entity_id=entity_id).aggregate(
        average=Avg("stars"),
        count=Count("id"),
    )
    return {
        "average": round(result["average"] or 0, 1),
        "count": result["count"],
    }


def get_user_review_for_entity(user, entity_type: str, entity_id):
    return Review.objects.filter(user=user, entity_type=entity_type, entity_id=entity_id).first()
