import logging
import math
from .providers.nominatim import nominatim_provider

logger = logging.getLogger(__name__)


class MapsService:
    def geocode_address(self, address: str) -> dict:
        result = nominatim_provider.geocode(address)
        if result:
            return {"latitude": result["lat"], "longitude": result["lon"]}
        return {"latitude": None, "longitude": None}

    def reverse_geocode(self, lat: float, lon: float) -> dict:
        return nominatim_provider.reverse_geocode(lat, lon) or {}

    def calculate_distance(self, origin: tuple, destination: tuple) -> float | None:
        lat1, lon1 = origin
        lat2, lon2 = destination
        R = 6371.0
        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)
        a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
        return round(2 * R * math.asin(math.sqrt(a)), 2)

    def get_nearby_places(self, latitude: float, longitude: float, radius_km: float = 10) -> list:
        from .providers.overpass import overpass_provider
        return overpass_provider.search_nearby(latitude, longitude, int(radius_km * 1000))


maps_service = MapsService()
