import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)


def _send_html(*, subject, to, template, context, bcc=None):
    """
    Send a multipart (HTML + plain text fallback) email.
    Failures are logged, never raised.
    """
    if not to:
        return
    try:
        html_body = render_to_string(f"emails/{template}.html", context)

        msg = EmailMultiAlternatives(
            subject=subject,
            body="This email requires an HTML-capable email client.",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to] if isinstance(to, str) else to,
            bcc=bcc or [],
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send(fail_silently=False)
    except Exception:
        logger.exception(
            "Failed to send email | subject=%s | to=%s", subject, to
        )


def send_welcome_email(subscriber):
    """Sent immediately after a new subscriber signs up."""
    _send_html(
        subject="Welcome to Impactpreneur Global 👋",
        to=subscriber.email,
        template="welcome",
        context={"frontend_url": settings.FRONTEND_URL},
    )


def send_blog_notification(blog, subscribers):
    """
    Sent to all subscribers when a new blog is published.
    Subscribers go in BCC so they don't see each other's emails.
    """
    recipients = [s.email for s in subscribers]
    if not recipients:
        return

    blog_url = f"{settings.FRONTEND_URL.rstrip('/')}/blogs/{blog.id}"
    _send_html(
        subject=f"New Blog: {blog.title}",
        to=settings.DEFAULT_FROM_EMAIL,
        bcc=recipients,
        template="new_blog",
        context={"blog": blog, "blog_url": blog_url},
    )


def send_form_emails(*, form_name, submitter_email, submitter_name, details):
    """
    Sent on form submission:
      1. Confirmation to the submitter
      2. Notification to the team
    """
    _send_html(
        subject=f"We received your {form_name}",
        to=submitter_email,
        template="form_confirmation",
        context={
            "form_name": form_name,
            "submitter_name": submitter_name,
            "details": details,
        },
    )

    _send_html(
        subject=f"New {form_name} from {submitter_name}",
        to=settings.TEAM_EMAIL,
        template="team_notification",
        context={
            "form_name": form_name,
            "submitter_name": submitter_name,
            "details": details,
        },
    )