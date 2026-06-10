import math
import logging
from datetime import date
from decimal import Decimal
from django.utils import timezone

from .models import Recommendation, InteractionHistory

logger = logging.getLogger(__name__)

# ── Sprint 2 core weights (sum = 100) ────────────────────────────────────────
WEIGHT_PREFERENCE  = 40
WEIGHT_CATEGORY    = 25
WEIGHT_POPULARITY  = 15
WEIGHT_PROXIMITY   = 10
WEIGHT_INTERACTION = 10

# ── Sprint 3 contextual modifiers (additive, score clamped to [0, 100]) ─────
MOD_BUDGET_MATCH   =  10
MOD_BUDGET_OVER    = -10
MOD_PEOPLE_INVALID = -20
MOD_AGE_BLOCKED    = -50
MOD_TIME_BONUS     =   5
MOD_DISTANCE = {   # km → bonus
    2:  10,
    5:   8,
    10:  5,
    20:  2,
}


# ── Core scoring helpers ──────────────────────────────────────────────────────

def _pref_boost(category: str, activity_type: str = "", pref_map: dict = None) -> float:
    if not pref_map:
        return 0
    cat = category.lower()
    atype = activity_type.lower() if activity_type else ""
    for key, weight in pref_map.items():
        if key in cat or cat in key or (atype and (key in atype or atype in key)):
            return min(weight * (WEIGHT_PREFERENCE / 10), WEIGHT_PREFERENCE)
    return 0


def _category_score(category: str, pref_map: dict) -> float:
    cat = category.lower()
    for key in pref_map:
        if key in cat or cat in key:
            return WEIGHT_CATEGORY
    return 0


def _popularity_score(score_base: int) -> float:
    return min((score_base / 100) * WEIGHT_POPULARITY, WEIGHT_POPULARITY)


def _interaction_score(entity_id: str, interaction_set: set) -> float:
    return WEIGHT_INTERACTION if str(entity_id) in interaction_set else 0


def _weather_modifier(is_outdoor: bool, is_indoor: bool, is_outdoor_friendly) -> float:
    if is_outdoor_friendly is None:
        return 0
    if not is_outdoor_friendly:
        if is_indoor:
            return 10
        if is_outdoor and not is_indoor:
            return -10
    else:
        if is_outdoor:
            return 8
    return 0


# ── Sprint 3 contextual modifiers ────────────────────────────────────────────

def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def _distance_modifier(user_lat: float, user_lon: float, place_lat, place_lon) -> float:
    if user_lat is None or user_lon is None or place_lat is None or place_lon is None:
        return 0
    try:
        km = _haversine_km(user_lat, user_lon, float(place_lat), float(place_lon))
    except (TypeError, ValueError):
        return 0
    for threshold, bonus in sorted(MOD_DISTANCE.items()):
        if km <= threshold:
            return bonus
    return 0


def _budget_modifier(budget: float | None, min_cost: float | None) -> float:
    if budget is None or min_cost is None:
        return 0
    if min_cost <= budget:
        return MOD_BUDGET_MATCH
    if min_cost <= budget * 1.3:
        return 0
    return MOD_BUDGET_OVER


def _people_modifier(people: int | None, min_people: int, max_people: int | None) -> float:
    if people is None:
        return 0
    if people < min_people:
        return MOD_PEOPLE_INVALID
    if max_people is not None and people > max_people:
        return MOD_PEOPLE_INVALID
    return 0


def _age_modifier(user, minimum_age: int) -> float:
    if not minimum_age or minimum_age <= 0:
        return 0
    if not user.birth_date:
        return 0
    today = date.today()
    age = today.year - user.birth_date.year - (
        (today.month, today.day) < (user.birth_date.month, user.birth_date.day)
    )
    return MOD_AGE_BLOCKED if age < minimum_age else 0


def _time_of_day_modifier(is_indoor: bool, is_outdoor: bool, category: str) -> float:
    hour = timezone.localtime(timezone.now()).hour
    cat = category.lower()
    if 6 <= hour < 12:  # mañana
        if any(k in cat for k in ("café", "cafe", "desayuno", "breakfast", "outdoor", "park", "parque")):
            return MOD_TIME_BONUS
        if is_outdoor:
            return MOD_TIME_BONUS
    elif 12 <= hour < 19:  # tarde
        if any(k in cat for k in ("restaurant", "food", "gastronomía", "museo", "museum", "cine", "cinema")):
            return MOD_TIME_BONUS
    else:  # noche (19-6)
        if any(k in cat for k in ("bar", "music", "gaming", "concierto", "concert", "entertainment")):
            return MOD_TIME_BONUS
        if is_indoor:
            return 3
    return 0


def _build_reason(category: str, pref_map: dict, weather_used: bool, is_outdoor_friendly,
                  distance_km: float | None = None) -> str:
    parts = []
    cat = category.lower()
    for key in pref_map:
        if key in cat or cat in key:
            parts.append(f"coincide con tus preferencias de {key}")
            break
    if weather_used and is_outdoor_friendly is not None:
        parts.append("ideal para el clima de hoy" if not is_outdoor_friendly else "perfecto para salir con el clima actual")
    if distance_km is not None and distance_km <= 5:
        parts.append(f"a solo {distance_km:.1f} km de tu ubicación")
    if not parts:
        parts.append("popular entre usuarios similares")
    return ", ".join(parts).capitalize() + "."


# ── Main recommendation engine ────────────────────────────────────────────────

def generate_recommendations_for_user(
    user,
    lat: float = None,
    lon: float = None,
    budget: float = None,
    people: int = None,
) -> list:
    from apps.activities.selectors import get_active_activities
    from apps.events.selectors import get_published_events
    from apps.places.selectors import get_active_places
    from apps.users.selectors import get_user_preferences
    from apps.integrations.weather_service import weather_service

    # Resolve user location: query params take priority, then profile
    user_lat = lat if lat is not None else (float(user.latitude) if user.latitude else None)
    user_lon = lon if lon is not None else (float(user.longitude) if user.longitude else None)

    prefs = list(get_user_preferences(user))
    pref_map = {
        (p.value.lower() if p.value else p.category.lower()): p.weight
        for p in prefs
    }

    weather = {}
    if user_lat is not None and user_lon is not None:
        weather = weather_service.get_current_weather(user_lat, user_lon)
    is_outdoor_friendly = weather.get("is_outdoor_friendly")
    weather_used = is_outdoor_friendly is not None

    interaction_set = set(
        str(eid)
        for eid in InteractionHistory.objects.filter(user=user).values_list("entity_id", flat=True)
    )

    pending = []

    # ── Activities ────────────────────────────────────────────────────────────
    for activity in get_active_activities():
        place_lat = activity.place.latitude if activity.place_id else None
        place_lon = activity.place.longitude if activity.place_id else None
        distance_km = None
        if user_lat and place_lat:
            try:
                distance_km = _haversine_km(user_lat, user_lon, float(place_lat), float(place_lon))
            except Exception:
                pass

        min_cost = float(activity.min_budget) if activity.min_budget else None
        score = (
            _pref_boost(activity.category, activity.activity_type, pref_map)
            + _category_score(activity.category, pref_map)
            + _popularity_score(activity.score_base)
            + _interaction_score(activity.id, interaction_set)
            + _weather_modifier(activity.outdoor, activity.indoor, is_outdoor_friendly)
            + _distance_modifier(user_lat, user_lon, place_lat, place_lon)
            + _budget_modifier(budget, min_cost)
            + _people_modifier(people, activity.min_people, activity.max_people)
            + _time_of_day_modifier(activity.indoor, activity.outdoor, activity.category)
        )
        score = max(0, min(100, score))
        reason = _build_reason(activity.category, pref_map, weather_used, is_outdoor_friendly, distance_km)
        pending.append(Recommendation(
            user=user,
            activity=activity,
            score=Decimal(str(round(score, 2))),
            recommendation_reason=reason,
        ))

    # ── Events ────────────────────────────────────────────────────────────────
    now = timezone.now()
    for event in get_published_events():
        place_lat = event.place.latitude if event.place_id else None
        place_lon = event.place.longitude if event.place_id else None
        distance_km = None
        if user_lat and place_lat:
            try:
                distance_km = _haversine_km(user_lat, user_lon, float(place_lat), float(place_lon))
            except Exception:
                pass

        days_away = max(0, (event.start_date - now).days) if event.start_date > now else 99
        proximity_bonus = WEIGHT_PROXIMITY if 0 <= days_away <= 7 else 0
        event_cost = float(event.price) if event.price else 0

        score = (
            _pref_boost(event.category, "", pref_map)
            + _category_score(event.category, pref_map)
            + _popularity_score(60)
            + proximity_bonus
            + _interaction_score(event.id, interaction_set)
            + _distance_modifier(user_lat, user_lon, place_lat, place_lon)
            + _budget_modifier(budget, event_cost)
            + _age_modifier(user, event.minimum_age)
            + _time_of_day_modifier(is_indoor=True, is_outdoor=False, category=event.category)
        )
        score = max(0, min(100, score))
        reason = _build_reason(event.category, pref_map, False, None, distance_km)
        pending.append(Recommendation(
            user=user,
            event=event,
            score=Decimal(str(round(score, 2))),
            recommendation_reason=reason,
        ))

    # ── Places ────────────────────────────────────────────────────────────────
    for place in get_active_places():
        distance_km = None
        if user_lat and place.latitude:
            try:
                distance_km = _haversine_km(user_lat, user_lon, float(place.latitude), float(place.longitude))
            except Exception:
                pass

        score = (
            _pref_boost(place.category, "", pref_map)
            + _category_score(place.category, pref_map)
            + _popularity_score(50)
            + _interaction_score(place.id, interaction_set)
            + _distance_modifier(user_lat, user_lon, place.latitude, place.longitude)
            + _time_of_day_modifier(is_indoor=True, is_outdoor=False, category=place.category)
        )
        score = max(0, min(100, score))
        reason = _build_reason(place.category, pref_map, False, None, distance_km)
        pending.append(Recommendation(
            user=user,
            place=place,
            score=Decimal(str(round(score, 2))),
            recommendation_reason=reason,
        ))

    Recommendation.objects.filter(user=user).delete()
    pending.sort(key=lambda r: r.score, reverse=True)
    Recommendation.objects.bulk_create(pending[:20])

    from apps.audit.services import log_action
    log_action(
        user=user,
        action="recommendation_generated",
        entity_type="recommendation",
        entity_id=str(user.id),
        metadata={"count": min(len(pending), 20)},
    )

    return list(
        Recommendation.objects
        .filter(user=user)
        .select_related("activity", "event", "place", "event__place", "activity__place")
        .order_by("-score")[:20]
    )


def log_interaction(*, user, action: str, entity_type: str, entity_id: str) -> InteractionHistory:
    return InteractionHistory.objects.create(
        user=user,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
    )
