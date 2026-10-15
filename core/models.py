from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings

class ContactSubject(models.TextChoices):
    GENERAL = "General Inquiry", "General Inquiry"
    PARTNERSHIP = "Partnership Opportunities", "Partnership Opportunities"
    SCALING = "Scaling & Mentorship", "Scaling & Mentorship"
    TECHNICAL = "Technical Support", "Technical Support"


class Program(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = CloudinaryField('image')  # changed from ImageField
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ["-created_at"]
    def __str__(self):
        return self.title


class Blog(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
     
    image = CloudinaryField('image')  # changed from ImageField
    date = models.DateField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blogs",
        null=True,       # temporary: existing rows have no author
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    bio = models.TextField()
    image = CloudinaryField('image')  # changed from ImageField

    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.email


class ServiceRequest(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=100)
    service = models.CharField(max_length=200)
    organization_name = models.CharField(max_length=200, blank=True)
    stage = models.CharField(max_length=100, blank=True)
    help_description = models.TextField()
    budget_range = models.CharField(max_length=100, blank=True)
    timeline = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.service}"


class ContactMessage(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(
        max_length=200,
        choices=ContactSubject.choices,
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - {self.subject}"


class CommunityApplication(models.Model):
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    organization_name = models.CharField(max_length=200, blank=True)
    building_description = models.TextField()
    why_join = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.full_name} - Application"