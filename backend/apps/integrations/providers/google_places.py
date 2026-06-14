import logging
import requests
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_TTL = 86400  # 24 hours
TIMEOUT = 3


class GooglePlacesProvider:
    NEARBY_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    TEXT_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"

    def _api_key(self) -> str:
        return getattr(settings, "GOOGLE_PLACES_API_KEY", "")

    def search_nearby(
        self,
        lat: float,
        lon: float,
        radius: int = 1500,
        place_type: str = "",
    ) -> list[dict]:
        api_key = self._api_key()
        if not api_key:
            return []

        lat_r = round(lat, 4)
        lon_r = round(lon, 4)
        cache_key = f"google_places:{lat_r}:{lon_r}:{radius}:{place_type}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        params = {
            "location": f"{lat_r},{lon_r}",
            "radius": radius,
            "key": api_key,
        }
        if place_type:
            params["type"] = place_type

        try:
            resp = requests.get(self.NEARBY_URL, params=params, timeout=TIMEOUT)
            resp.raise_for_status()
            results = self._parse_results(resp.json().get("results", []))
            cache.set(cache_key, results, CACHE_TTL)
            return results
        except Exception as exc:
            logger.warning("GooglePlacesProvider.search_nearby error: %s", exc)
            return []

    def search_by_query(self, query: str, lat: float, lon: float) -> list[dict]:
        api_key = self._api_key()
        if not api_key:
            return []

        lat_r = round(lat, 4)
        lon_r = round(lon, 4)
        cache_key = f"google_places_text:{query}:{lat_r}:{lon_r}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        params = {
            "query": query,
            "location": f"{lat_r},{lon_r}",
            "radius": 5000,
            "key": api_key,
        }

        try:
            resp = requests.get(self.TEXT_URL, params=params, timeout=TIMEOUT)
            resp.raise_for_status()
            results = self._parse_results(resp.json().get("results", []))
            cache.set(cache_key, results, CACHE_TTL)
            return results
        except Exception as exc:
            logger.warning("GooglePlacesProvider.search_by_query error: %s", exc)
            return []

    def _parse_results(self, raw: list) -> list[dict]:
        parsed = []
        for item in raw:
            loc = item.get("geometry", {}).get("location", {})
            parsed.append({
                "external_id": item.get("place_id", ""),
                "name": item.get("name", ""),
                "address": item.get("vicinity") or item.get("formatted_address", ""),
                "latitude": loc.get("lat"),
                "longitude": loc.get("lng"),
                "category": self._map_type(item.get("types", [])),
                "price_level": item.get("price_level", 0),
                "source": "google",
            })
        return parsed

    @staticmethod
    def _map_type(types: list) -> str:
        mapping = {
            "restaurant": "Gastronomía",
            "bar": "Bar",
            "cafe": "Café",
            "museum": "Museo",
            "park": "Parque",
            "shopping_mall": "Shopping",
            "movie_theater": "Cine",
            "gym": "Deporte",
            "night_club": "Entretenimiento",
            "tourist_attraction": "Turismo",
            "lodging": "Alojamiento",
            "hospital": "Salud",
            "pharmacy": "Salud",
        }
        for t in types:
            if t in mapping:
                return mapping[t]
        return "Lugar"


google_places_provider = GooglePlacesProvider()
