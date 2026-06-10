from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from apps.core.responses import success_response, created_response, no_content_response, error_response
from .serializers import FavoriteSerializer
from .selectors import get_user_favorites, get_favorite_by_id
from .services import add_favorite, remove_favorite


@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def favorite_list(request):
    if request.method == "GET":
        favorites = get_user_favorites(request.user)
        return success_response(FavoriteSerializer(favorites, many=True).data)

    serializer = FavoriteSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    fav = add_favorite(user=request.user, **serializer.validated_data)
    return created_response(FavoriteSerializer(fav).data)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def favorite_detail(request, pk):
    fav = get_favorite_by_id(pk, request.user)
    if not fav:
        return error_response("NOT_FOUND", "Favorito no encontrado.", status_code=status.HTTP_404_NOT_FOUND)
    remove_favorite(user=request.user, favorite=fav)
    return no_content_response()
