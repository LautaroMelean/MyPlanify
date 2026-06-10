# Google Maps / Geocoding API integration — Sprint 0 stub.
# Full implementation in Sprint 1.

import logging

logger = logging.getLogger(__name__)


class MapsService:
    def geocode_address(self, address: str) -> dict:
        logger.info("MapsService.geocode_address called (stub)")
        return {"latitude": None, "longitude": None}

    def calculate_distance(self, origin: tuple, destination: tuple) -> float:
        logger.info("MapsService.calculate_distance called (stub)")
        return None

    def get_nearby_places(self, latitude: float, longitude: float, radius_km: float = 10) -> list:
        logger.info("MapsService.get_nearby_places called (stub)")
        return []


maps_service = MapsService()
