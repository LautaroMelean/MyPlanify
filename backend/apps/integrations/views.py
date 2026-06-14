import logging
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.core.responses import success_response, error_response
from .providers.openweather import openweather_provider
from .services import get_external_places, search_external_places

logger = logging.getLogger(__name__)


def _parse_coord(value, name: str, lo: float, hi: float):
    if value is None:
        return None, None
    try:
        f = float(value)
    except (TypeError, ValueError):
        return None, f"{name} debe ser un número decimal."
    if not (lo <= f <= hi):
        return None, f"{name} fuera de rango ({lo}, {hi})."
    return f, None


class WeatherCurrentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lat, err = _parse_coord(request.query_params.get("lat"), "lat", -90, 90)
        if err:
            return error_response("INVALID_PARAM", err, status_code=status.HTTP_400_BAD_REQUEST)

        lon, err = _parse_coord(request.query_params.get("lon"), "lon", -180, 180)
        if err:
            return error_response("INVALID_PARAM", err, status_code=status.HTTP_400_BAD_REQUEST)

        if lat is None or lon is None:
            return error_response(
                "MISSING_PARAMS", "Se requieren lat y lon.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        weather = openweather_provider.get_current_weather(lat, lon)
        return success_response(weather)


class ExternalPlacesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        lat, err = _parse_coord(request.query_params.get("lat"), "lat", -90, 90)
        if err:
            return error_response("INVALID_PARAM", err, status_code=status.HTTP_400_BAD_REQUEST)

        lon, err = _parse_coord(request.query_params.get("lon"), "lon", -180, 180)
        if err:
            return error_response("INVALID_PARAM", err, status_code=status.HTTP_400_BAD_REQUEST)

        if lat is None or lon is None:
            return error_response(
                "MISSING_PARAMS", "Se requieren lat y lon.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        try:
            radius = int(request.query_params.get("radius", 1500))
            radius = max(100, min(radius, 50000))
        except (TypeError, ValueError):
            radius = 1500

        place_type = (request.query_params.get("type") or "")[:50]
        places = get_external_places(lat, lon, radius, place_type)
        return success_response([_serialize_place(p) for p in places])


class ExternalPlacesSearchView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = (request.query_params.get("q") or "").strip()[:200]
        if not query:
            return error_response(
                "MISSING_PARAMS", "Se requiere el parámetro q.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        lat, lat_err = _parse_coord(request.query_params.get("lat"), "lat", -90, 90)
        lon, lon_err = _parse_coord(request.query_params.get("lon"), "lon", -180, 180)

        if lat_err or lon_err or lat is None or lon is None:
            return error_response(
                "INVALID_PARAMS", "Se requieren lat y lon válidos.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        places = search_external_places(query, lat, lon)
        return success_response([_serialize_place(p) for p in places])


def _serialize_place(place) -> dict:
    return {
        "id": str(place.id),
        "name": place.name,
        "category": place.category,
        "address": place.address,
        "city": place.city,
        "latitude": float(place.latitude) if place.latitude else None,
        "longitude": float(place.longitude) if place.longitude else None,
        "phone": place.phone,
        "website": place.website,
        "image_url": place.image_url,
        "price_level": place.price_level,
        "source": place.source,
    }
