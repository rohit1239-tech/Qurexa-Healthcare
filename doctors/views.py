from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from appointments.models import Appointment
from .models import Doctor

@login_required
def doctor_dashboard(request):
    doctor = Doctor.objects.get(user=request.user)

    query = request.GET.get('q', '')
    appointments = Appointment.objects.filter(doctor=doctor)

    if query:
        appointments = appointments.filter(
            patient__user__username__icontains=query
        )

    return render(
        request,
        'doctors/dashboard.html',
        {
            'appointments': appointments,
            'query': query
        }
    )
