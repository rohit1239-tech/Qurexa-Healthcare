from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.timezone import now

from .models import Appointment
from patients.models import Patient
from doctors.models import Doctor
from records.models import Visit


# --------------------------------------------------
# PATIENT: BOOK APPOINTMENT
# --------------------------------------------------
@login_required
def book_appointment(request):
    # 🔒 Only PATIENT can book
    if request.user.role != 'PATIENT':
        return HttpResponseForbidden("Only patients can book appointments")

    # Get patient profile safely
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        return HttpResponseForbidden("Patient profile not found")

    if request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        appointment_date = request.POST.get('appointment_date')

        if not doctor_id or not appointment_date:
            return render(request, 'appointments/book.html', {
                'doctors': Doctor.objects.all(),
                'error': 'All fields are required'
            })

        doctor = get_object_or_404(Doctor, id=doctor_id)

        # 🚫 Prevent booking in the past
        if appointment_date < str(now()):
            return render(request, 'appointments/book.html', {
                'doctors': Doctor.objects.all(),
                'error': 'Cannot book appointment in the past'
            })

        # 🚫 Prevent double booking (same doctor, same time)
        if Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date
        ).exists():
            return render(request, 'appointments/book.html', {
                'doctors': Doctor.objects.all(),
                'error': 'Doctor already has an appointment at this time'
            })

        Appointment.objects.create(
            patient=patient,
            doctor=doctor,
            appointment_date=appointment_date,
            status='PENDING'
        )

        return redirect('patient_dashboard')

    doctors = Doctor.objects.all()
    return render(request, 'appointments/book.html', {'doctors': doctors})


# --------------------------------------------------
# DOCTOR: VIEW APPOINTMENTS
# --------------------------------------------------
@login_required
def doctor_appointments(request):
    # 🔒 Only DOCTOR can view
    if request.user.role != 'DOCTOR':
        return HttpResponseForbidden("Only doctors can view appointments")

    try:
        doctor = Doctor.objects.get(user=request.user)
    except Doctor.DoesNotExist:
        return render(request, 'appointments/doctor_list.html', {
            'error': 'Doctor profile not created. Contact admin.'
        })

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by('appointment_date')

    return render(request, 'appointments/doctor_list.html', {
        'appointments': appointments
    })


# --------------------------------------------------
# DOCTOR: UPDATE STATUS (Pending / Cancelled etc.)
# --------------------------------------------------
@login_required
def update_appointment_status(request, pk):
    if request.user.role != 'DOCTOR':
        return HttpResponseForbidden("Only doctors can update appointments")

    appointment = get_object_or_404(Appointment, id=pk)

    doctor = get_object_or_404(Doctor, user=request.user)

    if appointment.doctor != doctor:
        return HttpResponseForbidden("Not your appointment")

    if request.method == 'POST':
        new_status = request.POST.get('status')

        if new_status in ['PENDING', 'CANCELLED', 'COMPLETED']:
            appointment.status = new_status
            appointment.save()

    return redirect('doctor_appointments')


# --------------------------------------------------
# DOCTOR: COMPLETE APPOINTMENT (CREATE VISIT)
# --------------------------------------------------
@login_required
def complete_appointment(request, appointment_id):
    # 🔒 Only DOCTOR
    if request.user.role != 'DOCTOR':
        return HttpResponseForbidden("Only doctors can complete appointments")

    appointment = get_object_or_404(Appointment, id=appointment_id)

    doctor = get_object_or_404(Doctor, user=request.user)

    if appointment.doctor != doctor:
        return HttpResponseForbidden("Not your appointment")

    # Already completed?
    if appointment.status == 'COMPLETED':
        return redirect('doctor_appointments')

    # Mark appointment completed
    appointment.status = 'COMPLETED'
    appointment.save()

    # 🚑 Create Visit record automatically
    visit = Visit.objects.create(
        patient=appointment.patient,
        doctor=appointment.doctor,
        appointment=appointment,
        symptoms="",
        clinical_notes=""
    )

    # Redirect to clinical context page
    return redirect(f'/records/visit/{visit.id}/context/')
