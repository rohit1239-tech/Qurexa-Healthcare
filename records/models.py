from django.db import models
from patients.models import Patient
from doctors.models import Doctor
from appointments.models import Appointment


class Visit(models.Model):
    appointment = models.OneToOneField(
        Appointment,
        on_delete=models.CASCADE,
        limit_choices_to={'status': 'COMPLETED'}
    )

    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, editable=False)

    # Doctor written
    symptoms = models.TextField(blank=True)
    clinical_notes = models.TextField(blank=True)

    # AI
    ai_summary = models.TextField(blank=True)

    is_finalized = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.patient = self.appointment.patient
        self.doctor = self.appointment.doctor
        super().save(*args, **kwargs)

    def previous_visits(self):
        return Visit.objects.filter(
            patient=self.patient
        ).exclude(id=self.id).order_by('-created_at')

    def __str__(self):
        return f"{self.patient.user.username} | {self.created_at.date()}"
