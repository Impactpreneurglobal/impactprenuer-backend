from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Blog, Subscriber


@receiver(post_save, sender=Blog)
def notify_subscribers_on_new_blog(sender, instance, created, **kwargs):
    """
    When a new Blog is created, email all subscribers with a CTA link to it.
    Only fires on creation (created=True), not on updates.
    """
    if not created:
        return

    subscribers = Subscriber.objects.values_list("email", flat=True)
    recipients = list(subscribers)
    if not recipients:
        return

    blog_url = f"{settings.FRONTEND_URL.rstrip('/')}/blogs/{instance.id}"
    subject = f"New Blog: {instance.title}"
    message = (
        f"Hi there,\n\n"
        f"We just published a new blog post: {instance.title}\n\n"
        f"{instance.description}\n\n"
        f"Read it here: {blog_url}\n\n"
        f"— The Impactpreneur Team"
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipients,
        fail_silently=False,
    )