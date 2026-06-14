import logging
import math
from django.utils import timezone
from django.db.models import Q

from apps.places.models import Place
from .providers.google_places import google_places_provider

logger = logging.getLogger(__name__)

SYNC_STALE_HOURS = 24


def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def _is_stale(place: Place) -> bool:
    if place.last_synced_at is None:
        return True
    delta = timezone.now() - place.last_synced_at
    return delta.total_seconds() > SYNC_STALE_HOURS * 3600


def get_external_places(lat: float, lon: float, radius: int = 1500, place_type: str = "") -> list:
    """Return nearby Google-sourced places, fetching from API only when cache/DB is stale."""
    stale_threshold = timezone.now() - timezone.timedelta(hours=SYNC_STALE_HOURS)
    db_places = list(
        Place.objects.filter(
            source="google",
            is_active=True,
            last_synced_at__gte=stale_threshold,
            latitude__isnull=False,
            longitude__isnull=False,
        )
    )

    nearby_db = [
        p for p in db_places
        if _haversine_km(lat, lon, float(p.latitude), float(p.longitude)) <= radius / 1000
    ]

    if nearby_db:
        return nearby_db

    raw_results = google_places_provider.search_nearby(lat, lon, radius, place_type)
    return _upsert_places(raw_results)


def search_external_places(query: str, lat: float, lon: float) -> list:
    """Text search through Google Places, fallback to internal places on failure."""
    raw_results = google_places_provider.search_by_query(query, lat, lon)
    if not raw_results:
        return list(
            Place.objects.filter(is_active=True, name__icontains=query).order_by("name")[:20]
        )
    return _upsert_places(raw_results)


def _upsert_places(raw_results: list) -> list:
    now = timezone.now()
    places = []
    for item in raw_results:
        if not item.get("external_id") or not item.get("latitude") or not item.get("longitude"):
            continue
        place, _ = Place.objects.update_or_create(
            external_id=item["external_id"],
            defaults={
                "name": item["name"],
                "address": item["address"],
                "city": "",
                "latitude": item["latitude"],
                "longitude": item["longitude"],
                "category": item["category"],
                "price_level": item.get("price_level", 0),
                "source": "google",
                "last_synced_at": now,
                "is_active": True,
            },
        )
        places.append(place)
    return places
