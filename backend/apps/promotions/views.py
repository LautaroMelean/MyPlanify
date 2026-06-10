from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.core.responses import success_response, created_response, no_content_response, error_response
from .serializers import PromotionSerializer, PromotionCreateSerializer
from .selectors import get_active_promotions, get_promotion_by_id
from .services import create_promotion, update_promotion, delete_promotion, activate_promotion, cancel_promotion
from .permissions import PromotionPermission


@api_view(["GET", "POST"])
@permission_classes([PromotionPermission])
def promotion_list(request):
    if request.method == "GET":
        place_id = request.query_params.get("place")
        promotions = get_active_promotions(place_id=place_id)
        return success_response(PromotionSerializer(promotions, many=True).data)

    serializer = PromotionCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    promo = create_promotion(user=request.user, **serializer.validated_data)
    return created_response(PromotionSerializer(promo).data)


@api_view(["GET", "PATCH", "DELETE"])
@permission_classes([PromotionPermission])
def promotion_detail(request, pk):
    promo = get_promotion_by_id(pk)
    if not promo:
        return error_response("NOT_FOUND", "Promoción no encontrada.", status_code=status.HTTP_404_NOT_FOUND)

    if not PromotionPermission().has_object_permission(request, None, promo):
        return error_response("PERMISSION_DENIED", "Acceso denegado.", status_code=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        return success_response(PromotionSerializer(promo).data)

    if request.method == "PATCH":
        serializer = PromotionCreateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        promo = update_promotion(user=request.user, promotion=promo, **serializer.validated_data)
        return success_response(PromotionSerializer(promo).data)

    delete_promotion(user=request.user, promotion=promo)
    return no_content_response()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def promotion_activate(request, pk):
    promo = get_promotion_by_id(pk)
    if not promo:
        return error_response("NOT_FOUND", "Promoción no encontrada.", status_code=status.HTTP_404_NOT_FOUND)
    promo = activate_promotion(user=request.user, promotion=promo)
    return success_response(PromotionSerializer(promo).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def promotion_cancel(request, pk):
    promo = get_promotion_by_id(pk)
    if not promo:
        return error_response("NOT_FOUND", "Promoción no encontrada.", status_code=status.HTTP_404_NOT_FOUND)
    promo = cancel_promotion(user=request.user, promotion=promo)
    return success_response(PromotionSerializer(promo).data)
