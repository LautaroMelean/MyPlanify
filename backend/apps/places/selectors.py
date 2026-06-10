from .models import Place


def get_active_places(city=None, category=None):
    qs = Place.objects.filter(is_active=True)
    if city:
        qs = qs.filter(city__icontains=city)
    if category:
        qs = qs.filter(category=category)
    return qs.order_by("name")


def get_place_by_id(place_id):
    try:
        return Place.objects.get(id=place_id, is_active=True)
    except Place.DoesNotExist:
        return None
