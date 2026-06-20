from django.utils import timezone
from .models import Plan, PlanItem


def get_plans_for_user(user):
    return Plan.objects.filter(user=user).prefetch_related("items")


def get_plan_by_id(plan_id, user=None):
    try:
        qs = Plan.objects.prefetch_related("items")
        if user is not None:
            return qs.get(id=plan_id, user=user)
        return qs.get(id=plan_id)
    except (Plan.DoesNotExist, ValueError):
        return None


def get_plan_by_slug(slug: str):
    try:
        return Plan.objects.prefetch_related("items").get(slug=slug, is_public=True)
    except Plan.DoesNotExist:
        return None


def get_trending_plans(city=None, period="week", limit=10, exclude_user=None):
    from django.db.models import Count, Q
    from apps.recommendations.models import InteractionHistory

    today = timezone.now().date()
    if period == "today":
        since = today
    elif period == "weekend":
        since = today
    else:  # week default
        since = today - timezone.timedelta(days=7)

    plans_qs = Plan.objects.filter(is_public=True).prefetch_related("items")
    if city:
        plans_qs = plans_qs.filter(city__icontains=city)
    if exclude_user is not None:
        plans_qs = plans_qs.exclude(user=exclude_user)

    # annotate item count to filter plans with at least 1 item
    plans_qs = plans_qs.annotate(item_count=Count("items")).filter(item_count__gte=1)

    all_plans = list(plans_qs)
    plan_ids = [str(p.id) for p in all_plans]

    # Compute view/share counts from InteractionHistory
    interactions = InteractionHistory.objects.filter(
        entity_type="plan",
        entity_id__in=plan_ids,
        created_at__date__gte=since,
    ).values("entity_id", "action")

    view_counts: dict = {}
    share_counts: dict = {}
    for row in interactions:
        eid = row["entity_id"]
        if row["action"] == "plan_viewed":
            view_counts[eid] = view_counts.get(eid, 0) + 1
        elif row["action"] == "plan_shared":
            share_counts[eid] = share_counts.get(eid, 0) + 1

    scored = []
    for plan in all_plans:
        pid = str(plan.id)
        views = view_counts.get(pid, 0)
        shares = share_counts.get(pid, 0)
        score = views * 1 + shares * 3
        scored.append((score, views, shares, plan))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [(plan, views, shares) for _, views, shares, plan in scored[:limit]]
