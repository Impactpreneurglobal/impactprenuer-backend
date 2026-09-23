from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core import mail
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Subscriber, Blog

User = get_user_model()


class SubscriberAPITests(APITestCase):
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
        self.assertEqual(res.data["count"], 1)


class NewsletterNotificationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="author1", password="pass123"
        )
        Subscriber.objects.create(email="sub1@example.com")
        Subscriber.objects.create(email="sub2@example.com")
        mail.outbox = []  # clear any emails from setup

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
        self.assertCountEqual(
            email.to, ["sub1@example.com", "sub2@example.com"]
        )
        # CTA link present in body
        self.assertIn("/blogs/", email.body)

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