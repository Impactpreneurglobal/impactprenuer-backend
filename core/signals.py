import logging

from django.db.models.signals import post_save
from django.dispatch import receiver

from .emails import send_blog_notification
from .models import Blog, Subscriber

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Blog)
def notify_subscribers_on_new_blog(sender, instance, created, **kwargs):
    """
    When a new Blog is created, email all subscribers with a CTA link to it.
    Only fires on creation, not updates.
    """
    if not created:
        return

    subscribers = list(Subscriber.objects.all())
    if not subscribers:
        return

    try:
        send_blog_notification(instance, subscribers)
    except Exception:
        logger.exception(
            "Failed to notify subscribers for blog id=%s", instance.id
        )