from unittest.mock import patch
from django.core.cache import cache
from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Subscriber, Blog

User = get_user_model()

class ThrottleTests(APITestCase):
    def setUp(self):
        cache.clear()  # reset throttle counters between tests

    def test_anon_throttled_after_limit(self):
        url = reverse("subscriber-list")
        # must match REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]["anon"] in settings.py
        limit = 20

        for i in range(limit):
            res = self.client.post(url, {"email": f"u{i}@example.com"})
            self.assertEqual(
                res.status_code,
                status.HTTP_201_CREATED,
                msg=f"Request {i} unexpectedly failed: {res.status_code} {res.data}",
            )

        # 21st request → throttled
        res = self.client.post(url, {"email": "over@example.com"})
        self.assertEqual(res.status_code, status.HTTP_429_TOO_MANY_REQUESTS)


class SubscriberAPITests(APITestCase):
    def setUp(self):
        cache.clear()
    def test_subscribe_success(self):
        url = reverse("subscriber-list")
        res = self.client.post(url, {"email": "new@example.com"})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Subscriber.objects.filter(email="new@example.com").exists())
        self.assertIn("created_at", res.data)

    def test_duplicate_email_rejected(self):
        Subscriber.objects.create(email="dup@example.com")
        url = reverse("subscriber-list")
        res = self.client.post(url, {"email": "dup@example.com"})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_email_rejected(self):
        url = reverse("subscriber-list")
        res = self.client.post(url, {"email": "not-an-email"})
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_requires_admin(self):
        url = reverse("subscriber-list")
        res = self.client.get(url)
        self.assertIn(
            res.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_admin_can_list(self):
        Subscriber.objects.create(email="a@example.com")
        admin = User.objects.create_superuser(
            username="admin", password="pass123", email="admin@example.com"
        )
        self.client.force_authenticate(user=admin)
        url = reverse("subscriber-list")
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        # paginated response shape
        self.assertIn("results", res.data)
        self.assertEqual(res.data["count"], 1)
        self.assertEqual(len(res.data["results"]), 1)


class NewsletterNotificationTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(
            username="author1", password="pass123"
        )
        Subscriber.objects.create(email="sub1@example.com")
        Subscriber.objects.create(email="sub2@example.com")
        mail.outbox = []

    def test_blog_creation_emails_all_subscribers(self):
        Blog.objects.create(
            title="Test Blog",
            description="A test",
            date="2026-01-01",
            author=self.user,
        )

        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("Test Blog", email.subject)
        self.assertCountEqual(email.bcc, ["sub1@example.com", "sub2@example.com"])
        self.assertNotIn("sub1@example.com", email.to)
        self.assertNotIn("sub2@example.com", email.to)

        html_parts = [c for c in email.alternatives if c[1] == "text/html"]
        self.assertEqual(len(html_parts), 1)
        self.assertIn("Test Blog", html_parts[0][0])
        self.assertIn("/blogs/", html_parts[0][0])

    def test_blog_update_does_not_email(self):
        blog = Blog.objects.create(
            title="Original",
            description="desc",
            date="2026-01-01",
            author=self.user,
        )
        mail.outbox = []

        blog.title = "Updated"
        blog.save()

        self.assertEqual(len(mail.outbox), 0)

    def test_no_subscribers_no_email(self):
        Subscriber.objects.all().delete()
        mail.outbox = []

        Blog.objects.create(
            title="Solo",
            description="desc",
            date="2026-01-01",
            author=self.user,
        )

        self.assertEqual(len(mail.outbox), 0)


class WelcomeEmailTests(APITestCase):
    def setUp(self):
        cache.clear()
        mail.outbox = []

    def test_subscribe_sends_welcome_email(self):
        url = reverse("subscriber-list")
        res = self.client.post(url, {"email": "newbie@example.com"})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertIn("Welcome", email.subject)
        self.assertEqual(email.to, ["newbie@example.com"])

        html_parts = [c for c in email.alternatives if c[1] == "text/html"]
        self.assertEqual(len(html_parts), 1)
        self.assertIn("Impactpreneur", html_parts[0][0])

class FormEmailFailureTests(APITestCase):
    def setUp(self):
        cache.clear()
    """Form submission must succeed even if the email backend blows up."""

    @patch("core.emails.EmailMultiAlternatives", side_effect=Exception("SMTP down"))
    def test_service_request_saves_even_if_email_fails(self, mock_send):
        from .models import ServiceRequest
        url = reverse("service-request-list")
        payload = {
            "full_name": "Test User",
            "email": "test@example.com",
            "country": "Nigeria",
            "service": "Mentorship",
            "help_description": "Need help",
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            ServiceRequest.objects.filter(email="test@example.com").exists()
        )

class ContactMessageValidationTests(APITestCase):
    def setUp(self):
        cache.clear()

    def test_valid_subject_accepted(self):
        url = reverse("contact-list")
        payload = {
            "full_name": "Test",
            "email": "test@example.com",
            "subject": "Technical Support",
            "message": "Help",
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_invalid_subject_rejected(self):
        url = reverse("contact-list")
        payload = {
            "full_name": "Test",
            "email": "test@example.com",
            "subject": "Random nonsense",
            "message": "Help",
        }
        res = self.client.post(url, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("subject", res.data)