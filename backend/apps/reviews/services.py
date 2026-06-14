from .models import Review
from apps.audit.services import log_action


def create_or_update_review(*, user, entity_type: str, entity_id, stars: int, text: str = "") -> Review:
    review, created = Review.objects.update_or_create(
        user=user,
        entity_type=entity_type,
        entity_id=entity_id,
        defaults={"stars": stars, "text": text},
    )
    action = "create" if created else "update"
    log_action(
        user=user,
        action=f"review_{action}",
        entity_type=entity_type,
        entity_id=str(entity_id),
        metadata={"stars": stars},
    )
    return review


def delete_review(*, user, entity_type: str, entity_id) -> bool:
    deleted, _ = Review.objects.filter(user=user, entity_type=entity_type, entity_id=entity_id).delete()
    if deleted:
        log_action(user=user, action="review_delete", entity_type=entity_type, entity_id=str(entity_id))
    return deleted > 0
