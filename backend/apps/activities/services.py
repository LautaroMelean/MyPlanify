from .models import Activity
from apps.audit.services import log_action


def create_activity(*, user, **kwargs) -> Activity:
    activity = Activity.objects.create(**kwargs)
    log_action(user=user, action="create", entity_type="activity", entity_id=str(activity.id))
    return activity


def update_activity(*, user, activity: Activity, **kwargs) -> Activity:
    changed = list(kwargs.keys())
    for field, value in kwargs.items():
        setattr(activity, field, value)
    if changed:
        activity.save(update_fields=[*changed, "updated_at"])
    log_action(user=user, action="update", entity_type="activity", entity_id=str(activity.id))
    return activity


def deactivate_activity(*, user, activity: Activity) -> None:
    activity.soft_delete()
    log_action(user=user, action="deactivate", entity_type="activity", entity_id=str(activity.id))
