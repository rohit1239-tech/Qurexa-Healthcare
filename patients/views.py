from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from records.models import Visit
from patients.models import Patient
from django.utils.timezone import now

@login_required
def patient_dashboard(request):
    patient = Patient.objects.get(user=request.user)

    upcoming = Appointment.objects.filter(
        patient=patient,
        appointment_date__gte=now()
    ).order_by('appointment_date')

    visits = Visit.objects.filter(
        patient=patient
    ).order_by('-created_at')

    return render(request, 'patients/dashboard.html', {
        'upcoming': upcoming,
        'visits': visits
    })
