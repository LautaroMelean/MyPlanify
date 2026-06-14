from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from apps.core.responses import success_response, created_response, no_content_response, error_response
from .serializers import ReviewSerializer, ReviewCreateSerializer
from .selectors import get_reviews_for_entity, get_entity_rating, get_user_review_for_entity
from .services import create_or_update_review, delete_review


@api_view(["GET"])
@permission_classes([AllowAny])
def review_list(request, entity_type, entity_id):
    if entity_type not in ("place", "activity", "event"):
        return error_response("INVALID_ENTITY_TYPE", "Tipo de entidad inválido.", status_code=status.HTTP_400_BAD_REQUEST)
    reviews = get_reviews_for_entity(entity_type=entity_type, entity_id=entity_id)
    rating = get_entity_rating(entity_type=entity_type, entity_id=entity_id)
    my_review = None
    if request.user.is_authenticated:
        r = get_user_review_for_entity(user=request.user, entity_type=entity_type, entity_id=entity_id)
        if r:
            my_review = ReviewSerializer(r).data
    return success_response({
        "rating": rating,
        "my_review": my_review,
        "reviews": ReviewSerializer(reviews, many=True).data,
    })


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def review_create(request):
    serializer = ReviewCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    review = create_or_update_review(user=request.user, **serializer.validated_data)
    return created_response(ReviewSerializer(review).data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def review_delete(request, entity_type, entity_id):
    if entity_type not in ("place", "activity", "event"):
        return error_response("INVALID_ENTITY_TYPE", "Tipo de entidad inválido.", status_code=status.HTTP_400_BAD_REQUEST)
    deleted = delete_review(user=request.user, entity_type=entity_type, entity_id=entity_id)
    if not deleted:
        return error_response("NOT_FOUND", "Reseña no encontrada.", status_code=status.HTTP_404_NOT_FOUND)
    return no_content_response()
