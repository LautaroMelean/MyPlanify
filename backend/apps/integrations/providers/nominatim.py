import logging
import requests
from django.core.cache import cache

logger = logging.getLogger(__name__)

CACHE_TTL = 3600  # 1 hour
TIMEOUT = 5
BASE_URL = "https://nominatim.openstreetmap.org"
# Nominatim requires a descriptive User-Agent per usage policy
HEADERS = {"User-Agent": "Planify/1.0 (lautaromatiasmelean@gmail.com)"}


class NominatimProvider:
    def geocode(self, query: str) -> dict | None:
        """Place name / address → {lat, lon, display_name, city, country}"""
        cache_key = f"nominatim:geocode:{query.lower().strip()}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            resp = requests.get(
                f"{BASE_URL}/search",
                params={"q": query, "format": "json", "limit": 1, "addressdetails": 1},
                headers=HEADERS,
                timeout=TIMEOUT,
            )
            resp.raise_for_status()
            results = resp.json()
            if not results:
                return None
            parsed = self._parse(results[0])
            cache.set(cache_key, parsed, CACHE_TTL)
            return parsed
        except Exception as exc:
            logger.warning("NominatimProvider.geocode error: %s", exc)
            return None

    def reverse_geocode(self, lat: float, lon: float) -> dict | None:
        """Coordinates → {display_name, city, country}"""
        lat_r, lon_r = round(lat, 4), round(lon, 4)
        cache_key = f"nominatim:reverse:{lat_r}:{lon_r}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        try:
            resp = requests.get(
                f"{BASE_URL}/reverse",
                params={"lat": lat_r, "lon": lon_r, "format": "json", "addressdetails": 1},
                headers=HEADERS,
                timeout=TIMEOUT,
            )
            resp.raise_for_status()
            data = resp.json()
            if "error" in data:
                return None
            parsed = self._parse(data)
            cache.set(cache_key, parsed, CACHE_TTL)
            return parsed
        except Exception as exc:
            logger.warning("NominatimProvider.reverse_geocode error: %s", exc)
            return None

    def _parse(self, data: dict) -> dict:
        address = data.get("address", {})
        city = (
            address.get("city")
            or address.get("town")
            or address.get("village")
            or address.get("municipality")
            or ""
        )
        return {
            "lat": float(data["lat"]),
            "lon": float(data["lon"]),
            "display_name": data.get("display_name", ""),
            "city": city,
            "country": address.get("country", ""),
            "country_code": address.get("country_code", ""),
        }


nominatim_provider = NominatimProvider()
