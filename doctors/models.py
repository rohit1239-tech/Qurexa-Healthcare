from django.db import models
from django.conf import settings

class Doctor(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)  # ✅ FIX

    def __str__(self):
        return self.user.username
