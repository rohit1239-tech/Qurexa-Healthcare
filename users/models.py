from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('DOCTOR', 'Doctor'),
        ('PATIENT', 'Patient'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='PATIENT'  # ✅ safety default
    )

    mobile = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


class OTP(models.Model):
    PURPOSE_CHOICES = (
        ('SIGNUP', 'Signup'),
        ('LOGIN', 'Login'),
    )

    contact = models.CharField(max_length=50)  
    # email OR mobile

    otp = models.CharField(max_length=6)

    purpose = models.CharField(
        max_length=10,
        choices=PURPOSE_CHOICES
    )

    created_at = models.DateTimeField(auto_now_add=True)

    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=5)

    def __str__(self):
        return f"{self.contact} | {self.otp} | {self.purpose}"
