import logging
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(name="apps.planner.tasks.plan_reminder_job")
def plan_reminder_job():
    """
    Runs hourly. Sends notifications for plans happening today or tomorrow.
    Avoids duplicate notifications using a simple flag on the plan.
    """
    from apps.planner.models import Plan
    from apps.notifications.models import Notification, NotificationType

    today = timezone.now().date()
    tomorrow = today + timezone.timedelta(days=1)

    day_of_plans = list(Plan.objects.filter(
        date=today, status__in=("generated", "planned"),
    ).select_related("user"))

    tomorrow_plans = list(Plan.objects.filter(
        date=tomorrow, status__in=("generated", "planned"),
    ).select_related("user"))

    all_plan_ids = [str(p.id) for p in day_of_plans + tomorrow_plans]

    # Pre-fetch all already-sent notifications in one query
    sent_titles = set(
        Notification.objects.filter(
            notification_type=NotificationType.SYSTEM,
            title__in=[f"Plan de hoy [{pid}]" for pid in all_plan_ids]
                      + [f"Plan de mañana [{pid}]" for pid in all_plan_ids],
        ).values_list("title", flat=True)
    )

    new_notifications = []
    for plan in day_of_plans:
        title = f"Plan de hoy [{plan.id}]"
        if title not in sent_titles:
            new_notifications.append(Notification(
                user=plan.user,
                title=title,
                message=f"Hoy tenés un plan programado: {plan.title}",
                notification_type=NotificationType.SYSTEM,
            ))
            logger.info("Day-of reminder queued for plan %s", plan.id)

    for plan in tomorrow_plans:
        title = f"Plan de mañana [{plan.id}]"
        if title not in sent_titles:
            new_notifications.append(Notification(
                user=plan.user,
                title=title,
                message=f"Tu plan para mañana está listo: {plan.title}",
                notification_type=NotificationType.SYSTEM,
            ))
            logger.info("Day-before reminder queued for plan %s", plan.id)

    if new_notifications:
        Notification.objects.bulk_create(new_notifications)

    return {
        "day_of": len(day_of_plans),
        "day_before": len(tomorrow_plans),
        "sent": len(new_notifications),
    }


@shared_task(name="apps.planner.tasks.plan_completion_job")
def plan_completion_job():
    """
    Runs hourly. Marks plans whose date has passed as 'completed'.
    Also registers plan_completed in InteractionHistory to feed Recommendation Engine V3.
    """
    from apps.planner.models import Plan
    from apps.recommendations.services import log_interaction

    yesterday = timezone.now().date() - timezone.timedelta(days=1)

    expired_plans = list(Plan.objects.filter(
        date__lte=yesterday,
        status__in=("generated", "planned"),
    ).select_related("user"))

    for plan in expired_plans:
        log_interaction(
            user=plan.user,
            action="plan_completed",
            entity_type="plan",
            entity_id=str(plan.id),
        )
        logger.info("Plan %s marked as completed", plan.id)

    if expired_plans:
        Plan.objects.filter(id__in=[p.id for p in expired_plans]).update(
            status="completed",
            updated_at=timezone.now(),
        )

    return {"completed": len(expired_plans)}
