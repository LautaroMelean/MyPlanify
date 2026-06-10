from django.utils import timezone
from .models import Event, EventStatus


def get_published_events(category=None, date_from=None, date_to=None, city=None):
    qs = Event.objects.filter(status=EventStatus.PUBLISHED, start_date__gte=timezone.now())
    if category:
        qs = qs.filter(category__icontains=category)
    if date_from:
        qs = qs.filter(start_date__date__gte=date_from)
    if date_to:
        qs = qs.filter(start_date__date__lte=date_to)
    if city:
        qs = qs.filter(place__city__icontains=city)
    return qs.select_related("place", "organizer").order_by("start_date")


def get_event_by_id(event_id):
    try:
        return Event.objects.select_related("place", "organizer").get(id=event_id)
    except Event.DoesNotExist:
        return None
