from rest_framework.exceptions import ValidationError, PermissionDenied

from .models import Promotion, PromotionStatus
from apps.audit.services import log_action


def create_promotion(*, user, **kwargs) -> Promotion:
    promo = Promotion.objects.create(owner=user, **kwargs)
    log_action(user=user, action="create", entity_type="promotion", entity_id=str(promo.id))
    return promo


def update_promotion(*, user, promotion: Promotion, **kwargs) -> Promotion:
    if not (user.role in ("admin", "moderator") or promotion.owner == user):
        raise PermissionDenied("No tenés permiso para editar esta promoción.")
    changed = list(kwargs.keys())
    for field, value in kwargs.items():
        setattr(promotion, field, value)
    if changed:
        promotion.save(update_fields=[*changed, "updated_at"])
    log_action(user=user, action="update", entity_type="promotion", entity_id=str(promotion.id))
    return promotion


def delete_promotion(*, user, promotion: Promotion) -> None:
    if not (user.role in ("admin", "moderator") or promotion.owner == user):
        raise PermissionDenied("No tenés permiso para eliminar esta promoción.")
    if promotion.status in (PromotionStatus.EXPIRED,):
        raise ValidationError({"status": "No se puede eliminar una promoción vencida."})
    promotion.status = PromotionStatus.CANCELLED
    promotion.save(update_fields=["status", "updated_at"])
    log_action(user=user, action="delete", entity_type="promotion", entity_id=str(promotion.id))


def activate_promotion(*, user, promotion: Promotion) -> Promotion:
    if promotion.status != PromotionStatus.DRAFT:
        raise ValidationError({"status": "Solo se pueden activar promociones en estado borrador."})
    if not (user.role in ("admin", "moderator") or promotion.owner == user):
        raise PermissionDenied("No tenés permiso para activar esta promoción.")
    promotion.status = PromotionStatus.ACTIVE
    promotion.save(update_fields=["status", "updated_at"])
    log_action(user=user, action="activate", entity_type="promotion", entity_id=str(promotion.id))
    return promotion


def cancel_promotion(*, user, promotion: Promotion) -> Promotion:
    if promotion.status not in (PromotionStatus.DRAFT, PromotionStatus.ACTIVE):
        raise ValidationError({"status": "No se puede cancelar esta promoción."})
    if not (user.role in ("admin", "moderator") or promotion.owner == user):
        raise PermissionDenied("No tenés permiso para cancelar esta promoción.")
    promotion.status = PromotionStatus.CANCELLED
    promotion.save(update_fields=["status", "updated_at"])
    log_action(user=user, action="cancel", entity_type="promotion", entity_id=str(promotion.id))
    return promotion
