from django.utils import timezone
from .models import Promotion, PromotionStatus


def get_active_promotions(place_id=None):
    now = timezone.now()
    qs = Promotion.objects.filter(
        status=PromotionStatus.ACTIVE,
        start_date__lte=now,
        end_date__gte=now,
    )
    if place_id:
        qs = qs.filter(place_id=place_id)
    return qs.select_related("place").order_by("-start_date")


def get_promotion_by_id(promotion_id):
    try:
        return Promotion.objects.select_related("place").get(id=promotion_id)
    except Promotion.DoesNotExist:
        return None
