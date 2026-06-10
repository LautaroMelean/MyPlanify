from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from apps.core.responses import success_response
from .serializers import RecommendationSerializer
from .services import generate_recommendations_for_user, log_interaction


def _parse_float(value):
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _parse_int(value):
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def recommendation_list(request):
    lat    = _parse_float(request.query_params.get("lat"))
    lon    = _parse_float(request.query_params.get("lon"))
    budget = _parse_float(request.query_params.get("budget"))
    people = _parse_int(request.query_params.get("people"))

    recommendations = generate_recommendations_for_user(
        request.user,
        lat=lat,
        lon=lon,
        budget=budget,
        people=people,
    )

    for rec in recommendations[:5]:
        entity_id = str(rec.activity_id or rec.event_id or rec.place_id)
        if entity_id and entity_id != "None":
            entity_type = "activity" if rec.activity_id else ("event" if rec.event_id else "place")
            log_interaction(user=request.user, action="view", entity_type=entity_type, entity_id=entity_id)

    return success_response(RecommendationSerializer(recommendations, many=True).data)
