from .models import Activity


def get_active_activities(activity_type=None, indoor=None, outdoor=None, budget=None, category=None):
    qs = Activity.objects.filter(is_active=True).select_related("place")
    if activity_type:
        qs = qs.filter(activity_type=activity_type)
    if category:
        qs = qs.filter(category__icontains=category)
    if indoor is not None:
        val = str(indoor).lower() in ("true", "1")
        qs = qs.filter(indoor=val)
    if outdoor is not None:
        val = str(outdoor).lower() in ("true", "1")
        qs = qs.filter(outdoor=val)
    if budget is not None:
        try:
            qs = qs.filter(min_budget__lte=float(budget))
        except (ValueError, TypeError):
            pass
    return qs.order_by("-score_base")


def get_activity_by_id(activity_id):
    try:
        return Activity.objects.select_related("place").get(id=activity_id, is_active=True)
    except Activity.DoesNotExist:
        return None
