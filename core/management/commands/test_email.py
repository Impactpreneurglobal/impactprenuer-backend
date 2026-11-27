"""
Send a test email to verify SMTP configuration.

Usage:
    python manage.py test_email                  # sends to TEAM_EMAIL
    python manage.py test_email you@example.com  # sends to a specific address
"""

from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Send a test email to verify SMTP is configured correctly."

    def add_arguments(self, parser):
        parser.add_argument(
            "recipient",
            nargs="?",
            type=str,
            help="Recipient email address. Defaults to settings.TEAM_EMAIL.",
        )

    def handle(self, *args, **options):
        recipient = options["recipient"] or settings.TEAM_EMAIL

        # Report config (password hidden)
        self.stdout.write("── Email config ────────────────────────")
        self.stdout.write(f"  EMAIL_BACKEND      : {settings.EMAIL_BACKEND}")
        self.stdout.write(f"  EMAIL_HOST         : {getattr(settings, 'EMAIL_HOST', '(unset)')}")
        self.stdout.write(f"  EMAIL_PORT         : {getattr(settings, 'EMAIL_PORT', '(unset)')}")
        self.stdout.write(f"  EMAIL_USE_TLS      : {getattr(settings, 'EMAIL_USE_TLS', '(unset)')}")
        self.stdout.write(f"  EMAIL_HOST_USER    : {getattr(settings, 'EMAIL_HOST_USER', '(unset)')}")
        self.stdout.write(f"  DEFAULT_FROM_EMAIL : {settings.DEFAULT_FROM_EMAIL}")
        self.stdout.write(f"  Recipient          : {recipient}")
        self.stdout.write("────────────────────────────────────────")

        try:
            sent = send_mail(
                subject="Impactpreneur SMTP test ✅",
                message=(
                    "If you're reading this, SMTP is configured correctly.\n\n"
                    "— Impactpreneur backend"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[recipient],
                fail_silently=False,
            )
        except Exception as exc:
            raise CommandError(f"❌ SMTP send failed: {exc}")

        if sent:
            self.stdout.write(self.style.SUCCESS(f"✅ Email sent to {recipient}"))
        else:
            self.stdout.write(self.style.WARNING("⚠️  No email sent (0 returned)."))