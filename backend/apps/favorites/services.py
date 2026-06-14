from rest_framework.exceptions import ValidationError

from .models import Favorite
from apps.audit.services import log_action


def add_favorite(*, user, event=None, place=None, activity=None) -> Favorite:
    if Favorite.objects.filter(user=user, event=event, place=place, activity=activity).exists():
        raise ValidationError("Este ítem ya está en tus favoritos.")
    favorite = Favorite(user=user, event=event, place=place, activity=activity)
    favorite.save()
    log_action(user=user, action="favorite", entity_type="favorite", entity_id=str(favorite.id))

    # Registrar interacción para mejorar futuras recomendaciones
    from apps.recommendations.services import log_interaction
    entity = event or place or activity
    if entity:
        entity_type = "event" if event else ("place" if place else "activity")
        log_interaction(user=user, action="favorite", entity_type=entity_type, entity_id=str(entity.id))

    return favorite


def remove_favorite(*, user, favorite: Favorite) -> None:
    if favorite.user != user:
        from rest_framework.exceptions import PermissionDenied
        raise PermissionDenied("No podés eliminar el favorito de otro usuario.")
    log_action(user=user, action="unfavorite", entity_type="favorite", entity_id=str(favorite.id))

    from apps.recommendations.services import log_interaction
    entity = favorite.event or favorite.place or favorite.activity
    if entity:
        entity_type = "event" if favorite.event_id else ("place" if favorite.place_id else "activity")
        log_interaction(user=user, action="unfavorite", entity_type=entity_type, entity_id=str(entity.id))

    favorite.delete()
