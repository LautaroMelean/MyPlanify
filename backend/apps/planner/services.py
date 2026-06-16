import uuid
import logging
from datetime import date as date_type
from decimal import Decimal
from django.utils import timezone
from django.utils.text import slugify

from .models import Plan, PlanItem
from apps.audit.services import log_action

logger = logging.getLogger(__name__)

# Preferred categories per slot — used for slot bonus
SLOT_KEYWORDS = {
    "morning": ["café", "cafe", "desayuno", "breakfast", "park", "parque", "outdoor", "brunch", "coffee",
                "museo", "museum", "jardín", "jardin", "reserva", "botanico", "ciencias", "yoga"],
    "afternoon": ["restaurant", "museo", "museum", "tour", "arte", "art", "gastronomía", "food", "cultural",
                  "turismo", "tourism", "feria", "mercado", "tango", "caminito", "teatro", "colón"],
    "evening": ["bar", "music", "gaming", "concierto", "concert", "entertainment", "nightlife", "show",
                "teatro", "jazz", "milonga", "karaoke", "cervecería", "cocktail", "stand-up", "humor"],
}

# Categories that count as "something to do" (not just eating/drinking)
ACTIVITY_CATEGORIES = {
    "Museo", "Turismo", "Cultura", "Parque", "Deporte", "Entretenimiento",
    "museum", "tourism", "park", "sports", "concert", "gaming",
}

GASTRO_CATEGORIES = {"Gastronomía", "Café", "restaurant", "cafe"}
BAR_CATEGORIES = {"Bar", "bar"}


def _slot_bonus(slot: str, category: str, activity_type: str = "") -> float:
    keywords = SLOT_KEYWORDS.get(slot, [])
    text = (category + " " + activity_type).lower()
    for kw in keywords:
        if kw in text:
            return 15
    return 0


def _top_category(category: str, activity_type: str) -> str:
    """Returns a simplified category bucket for variety enforcement."""
    cat = category.lower()
    atype = activity_type.lower() if activity_type else ""
    if any(k in cat or k in atype for k in ("gastronomía", "restaurant", "fast_food", "food_court", "comida")):
        return "gastro"
    if any(k in cat or k in atype for k in ("café", "cafe", "coffee", "brunch", "desayuno")):
        return "cafe"
    if any(k in cat or k in atype for k in ("bar", "pub", "cervecería", "cocktail", "nightlife", "jazz")):
        return "bar"
    if any(k in cat or k in atype for k in ("museo", "museum", "cultura", "arte", "galería")):
        return "culture"
    if any(k in cat or k in atype for k in ("parque", "park", "jardín", "reserva", "outdoor")):
        return "outdoor"
    if any(k in cat or k in atype for k in ("deporte", "sports", "gym", "kayak", "bici", "running")):
        return "sport"
    if any(k in cat or k in atype for k in ("turismo", "tourism", "tour", "tango", "milonga", "feria")):
        return "tourism"
    if any(k in cat or k in atype for k in ("entretenimiento", "gaming", "escape", "bowling", "arcade", "concert", "show", "teatro")):
        return "entertainment"
    return "other"


def _generate_slug(plan_date: date_type, user_id) -> str:
    base = slugify(f"plan-{plan_date.strftime('%Y-%m-%d')}-{str(user_id)[:8]}")
    suffix = str(uuid.uuid4())[:8]
    return f"{base}-{suffix}"


def _build_item_reason(breakdown: dict, pref_map: dict, is_outdoor_friendly) -> str:
    from apps.recommendations.services import _build_reason_from_breakdown
    weather_data = {"is_outdoor_friendly": is_outdoor_friendly} if is_outdoor_friendly is not None else None
    return _build_reason_from_breakdown(breakdown, pref_map, weather_data)


def generate_plan(user, plan_date: date_type, budget: Decimal, people_count: int, city: str) -> Plan:
    """
    Generate a 3-slot itinerary plan for the given date.
    Enforces variety: no two slots share the same broad category.
    Prioritizes "do something" activities over pure gastronomy.
    Weather rule: ≤5 days from today → real OpenWeather; >5 days → neutral.
    """
    from apps.activities.models import Activity
    from apps.places.models import Place
    from apps.events.models import Event, EventStatus
    from apps.users.selectors import get_user_preferences
    from apps.recommendations.models import InteractionHistory
    from apps.recommendations.services import (
        _pref_boost,
        _popularity_score,
        _interaction_score_v2,
        _weather_modifier,
        _budget_modifier,
        _people_modifier,
    )
    from apps.integrations.providers.openweather import openweather_provider

    today = timezone.now().date()
    delta_days = (plan_date - today).days

    # Weather rule: ≤5 days → real API, >5 days → neutral
    is_outdoor_friendly = None
    if delta_days <= 5 and user.latitude and user.longitude:
        try:
            weather = openweather_provider.get_current_weather(
                float(user.latitude), float(user.longitude)
            )
            if weather:
                is_outdoor_friendly = weather.get("is_outdoor_friendly")
        except Exception as exc:
            logger.warning("Weather fetch failed for planner: %s", exc)

    prefs = list(get_user_preferences(user))
    pref_map = {
        (p.value.lower() if p.value else p.category.lower()): p.weight
        for p in prefs
    }
    interactions = list(
        InteractionHistory.objects.filter(user=user).values_list("entity_id", "action")
    )

    budget_per_slot = float(budget) / 3
    all_candidates = []

    # ── Activities — filter by own city field ─────────────────────────────────
    activity_qs = Activity.objects.filter(
        is_active=True,
        min_budget__lte=budget_per_slot,
        min_people__lte=people_count,
    ).select_related("place")
    if city:
        from django.db.models import Q
        activity_qs = activity_qs.filter(
            Q(city__icontains=city) | Q(city="")
        )

    for act in activity_qs[:60]:
        pref_s = _pref_boost(act.category, act.activity_type, pref_map)
        pop_s = _popularity_score(act.score_base)
        inter_s = _interaction_score_v2(act.id, interactions)
        weather_s = _weather_modifier(act.outdoor, act.indoor, is_outdoor_friendly)
        budget_s = _budget_modifier(budget_per_slot, float(act.min_budget))
        people_s = _people_modifier(people_count, act.min_people, act.max_people)

        breakdown = {
            "preference": pref_s, "popularity": pop_s, "interaction": inter_s,
            "weather": weather_s, "budget": budget_s, "people": people_s,
        }
        base_score = max(0, min(100, sum(breakdown.values())))

        # Activities get a +10 "do-something" bonus to prioritize over pure gastro
        activity_bonus = 10
        all_candidates.append({
            "base_score": base_score + activity_bonus,
            "breakdown": breakdown,
            "entity_type": "activity",
            "entity_id": act.id,
            "name": act.name,
            "category": act.category,
            "activity_type": act.activity_type,
            "top_cat": _top_category(act.category, act.activity_type),
        })

    # ── Places — order by name, expand pool to 80 ────────────────────────────
    place_qs = Place.objects.filter(is_active=True)
    if city:
        place_qs = place_qs.filter(city__icontains=city)
    # Exclude pharmacies, hospitals, supermarkets — not entertainment
    place_qs = place_qs.exclude(category__in=["Salud", "Alojamiento", "Shopping"])

    for place in place_qs.order_by("name")[:80]:
        pref_s = _pref_boost(place.category, "", pref_map)
        pop_s = max(0, 15 - place.price_level * 2)
        inter_s = _interaction_score_v2(place.id, interactions)

        # Outdoor-friendly bonus when weather is good
        outdoor_s = 5 if (place.outdoor_seating and is_outdoor_friendly) else 0

        breakdown = {
            "preference": pref_s, "popularity": pop_s, "interaction": inter_s,
            "weather": outdoor_s, "budget": 0, "people": 0,
        }
        base_score = max(0, min(100, sum(breakdown.values())))

        all_candidates.append({
            "base_score": base_score,
            "breakdown": breakdown,
            "entity_type": "place",
            "entity_id": place.id,
            "name": place.name,
            "category": place.category,
            "activity_type": "",
            "top_cat": _top_category(place.category, ""),
        })

    # ── Events on plan date ───────────────────────────────────────────────────
    event_qs = Event.objects.filter(
        status=EventStatus.PUBLISHED,
        price__lte=budget_per_slot,
        start_date__date=plan_date,
    )
    if city:
        event_qs = event_qs.filter(place__city__icontains=city)

    for event in event_qs[:15]:
        pref_s = _pref_boost(event.category, "", pref_map)
        inter_s = _interaction_score_v2(event.id, interactions)

        breakdown = {
            "preference": pref_s, "popularity": 20, "interaction": inter_s,
            "weather": 0, "budget": 10, "people": 0,
        }
        base_score = max(0, min(100, sum(breakdown.values())))

        all_candidates.append({
            "base_score": base_score,
            "breakdown": breakdown,
            "entity_type": "event",
            "entity_id": event.id,
            "name": event.title,
            "category": event.category,
            "activity_type": "",
            "top_cat": _top_category(event.category, ""),
        })

    # ── Pick top-1 per slot with variety enforcement ─────────────────────────
    # Ideal arc: morning=outdoor/culture/sport, afternoon=culture/gastro/tourism, evening=bar/entertainment
    SLOT_PREFERRED = {
        "morning":   {"outdoor", "culture", "sport", "tourism", "cafe"},
        "afternoon": {"culture", "tourism", "gastro", "other"},
        "evening":   {"bar", "entertainment", "other"},
    }

    used_ids: set = set()
    used_cats: set = set()
    slot_results: dict = {}

    for slot in ("morning", "afternoon", "evening"):
        preferred = SLOT_PREFERRED[slot]
        scored = []
        for c in all_candidates:
            if c["entity_id"] in used_ids:
                continue
            total = c["base_score"] + _slot_bonus(slot, c["category"], c.get("activity_type", ""))
            # Bonus for preferred category in this slot
            if c["top_cat"] in preferred:
                total += 12
            # Penalty for reusing same broad category
            if c["top_cat"] in used_cats:
                total -= 20
            scored.append((min(100, total), c))

        scored.sort(key=lambda x: x[0], reverse=True)

        if scored:
            _, best = scored[0]
            used_ids.add(best["entity_id"])
            used_cats.add(best["top_cat"])
            reason = _build_item_reason(best["breakdown"], pref_map, is_outdoor_friendly)
            slot_results[slot] = {
                "entity_type": best["entity_type"],
                "entity_id": best["entity_id"],
                "reason": reason,
            }

    title = f"Plan para {plan_date.strftime('%d/%m/%Y')}"
    slug = _generate_slug(plan_date, user.id)

    plan = Plan.objects.create(
        user=user,
        title=title,
        date=plan_date,
        budget=budget,
        people_count=people_count,
        city=city,
        slug=slug,
        is_public=False,
        status="generated",
    )

    for order, slot in enumerate(("morning", "afternoon", "evening")):
        if slot in slot_results:
            item_data = slot_results[slot]
            PlanItem.objects.create(
                plan=plan,
                entity_type=item_data["entity_type"],
                entity_id=item_data["entity_id"],
                slot=slot,
                order=order,
                generation_reason=item_data["reason"],
            )

    log_action(
        user=user,
        action="create_plan",
        entity_type="plan",
        entity_id=str(plan.id),
        metadata={"title": title, "date": str(plan_date), "city": city},
    )

    return plan


def create_empty_plan(user, plan_date, budget, people_count: int, city: str) -> Plan:
    slug = _generate_slug(plan_date, user.id)
    plan = Plan.objects.create(
        user=user,
        title=f"Plan para {plan_date.strftime('%d/%m/%Y')}",
        date=plan_date,
        budget=budget,
        people_count=people_count,
        city=city,
        slug=slug,
        status="draft",
    )
    log_action(
        user=user,
        action="create_plan",
        entity_type="plan",
        entity_id=str(plan.id),
        metadata={"title": plan.title, "date": str(plan_date), "city": city, "mode": "empty"},
    )
    return plan


def add_item(plan: Plan, entity_type: str, entity_id: str, slot: str, note: str = "") -> PlanItem:
    from rest_framework.exceptions import ValidationError as DRFValidationError
    from apps.places.models import Place
    from apps.activities.models import Activity
    from apps.events.models import Event

    model_map = {"place": Place, "activity": Activity, "event": Event}
    model = model_map.get(entity_type)
    if model is None or not model.objects.filter(id=entity_id).exists():
        raise DRFValidationError({"entity_id": f"No existe ningún {entity_type} con id {entity_id}."})

    order = PlanItem.objects.filter(plan=plan, slot=slot).count()
    return PlanItem.objects.create(
        plan=plan,
        entity_type=entity_type,
        entity_id=entity_id,
        slot=slot,
        order=order,
        note=note,
    )


def remove_item(item: PlanItem) -> None:
    item.delete()


def delete_plan(plan: Plan, user) -> None:
    log_action(
        user=user,
        action="delete_plan",
        entity_type="plan",
        entity_id=str(plan.id),
        metadata={"title": plan.title},
    )
    plan.delete()


def share_plan(plan: Plan, user) -> None:
    from apps.recommendations.services import log_interaction
    log_interaction(user=user, action="plan_shared", entity_type="plan", entity_id=str(plan.id))
    log_action(
        user=user, action="plan_shared",
        entity_type="plan", entity_id=str(plan.id),
        metadata={"slug": plan.slug},
    )


def clone_plan(source_plan: Plan, user, new_date) -> Plan:
    slug = _generate_slug(new_date, user.id)
    cloned = Plan.objects.create(
        user=user,
        title=source_plan.title,
        date=new_date,
        budget=source_plan.budget,
        people_count=source_plan.people_count,
        city=source_plan.city,
        slug=slug,
        is_public=False,
        status="draft",
    )
    for item in source_plan.items.all():
        PlanItem.objects.create(
            plan=cloned,
            entity_type=item.entity_type,
            entity_id=item.entity_id,
            slot=item.slot,
            order=item.order,
            note=item.note,
            generation_reason=item.generation_reason,
        )
    from apps.recommendations.services import log_interaction
    log_interaction(user=user, action="plan_cloned", entity_type="plan", entity_id=str(source_plan.id))
    log_action(
        user=user, action="plan_cloned",
        entity_type="plan", entity_id=str(cloned.id),
        metadata={"source_plan_id": str(source_plan.id), "date": str(new_date)},
    )
    return cloned


def generate_surprise_plan(user, plan_date=None) -> Plan:
    from datetime import date as date_type
    from decimal import Decimal
    from django.utils import timezone
    from apps.recommendations.services import log_interaction

    if plan_date is None:
        plan_date = (timezone.now() + timezone.timedelta(days=1)).date()

    last_plan = Plan.objects.filter(user=user).order_by("-created_at").first()
    city = last_plan.city if last_plan else "Buenos Aires"

    recent = list(Plan.objects.filter(user=user).order_by("-created_at").values_list("budget", flat=True)[:3])
    if recent:
        budget = Decimal(sum(float(b) for b in recent) / len(recent)).quantize(Decimal("0.01"))
    else:
        budget = Decimal("3000.00")

    plan = generate_plan(user=user, plan_date=plan_date, budget=budget, people_count=1, city=city)
    log_interaction(user=user, action="plan_surprise", entity_type="plan", entity_id=str(plan.id))
    return plan


def update_item(item: PlanItem, note: str = None, order: int = None) -> PlanItem:
    update_fields = []
    if note is not None:
        item.note = note
        update_fields.append("note")
    if order is not None:
        item.order = order
        update_fields.append("order")
    if update_fields:
        item.save(update_fields=update_fields)
    return item


def create_plan_feedback(plan: Plan, user, entity_type: str, entity_id: str, rating: int, comment: str = ""):
    from rest_framework.exceptions import ValidationError as DRFValidationError
    from .models import PlanFeedback
    from apps.recommendations.services import log_interaction

    if plan.user != user:
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("No podés dar feedback de un plan que no es tuyo.")

    if rating not in range(1, 6):
        raise DRFValidationError({"rating": "El rating debe estar entre 1 y 5."})

    feedback, created = PlanFeedback.objects.update_or_create(
        plan=plan,
        user=user,
        entity_type=entity_type,
        entity_id=entity_id,
        defaults={"rating": rating, "comment": comment},
    )

    log_interaction(
        user=user,
        action="plan_feedback",
        entity_type=entity_type,
        entity_id=str(entity_id),
    )
    log_action(
        user=user,
        action="plan_feedback",
        entity_type="plan",
        entity_id=str(plan.id),
        metadata={"entity_type": entity_type, "entity_id": str(entity_id), "rating": rating},
    )
    return feedback
