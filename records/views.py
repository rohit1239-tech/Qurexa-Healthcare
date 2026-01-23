from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Visit
from doctors.models import Doctor
from ai_engine.services import generate_clinical_summary


# =========================================================
# VISIT CONTEXT (Doctor + Patient view)
# =========================================================
@login_required
def visit_context(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    # 🔒 Access control
    if request.user.role == 'DOCTOR':
        if visit.doctor.user != request.user:
            return HttpResponseForbidden("Not your patient")
    elif request.user.role == 'PATIENT':
        if visit.patient.user != request.user:
            return HttpResponseForbidden("Access denied")
    else:
        return HttpResponseForbidden("Unauthorized")

    previous_visits = visit.previous_visits()

    # Doctor writes report
    if request.method == 'POST':
        if request.user.role != 'DOCTOR':
            return HttpResponseForbidden("Only doctors can edit")

        visit.symptoms = request.POST.get('symptoms', '')
        visit.clinical_notes = request.POST.get('clinical_notes', '')
        visit.save()

        if 'generate_ai' in request.POST:
            visit.ai_summary = generate_clinical_summary(visit)
            visit.save()

        if 'finalize' in request.POST:
            visit.is_finalized = True
            visit.save()

        return redirect('visit_context', visit_id=visit.id)

    return render(
        request,
        'records/visit_context.html',
        {
            'visit': visit,
            'previous_visits': previous_visits,
        }
    )


# =========================================================
# AI CLINICAL SUMMARY (Doctor only)
# =========================================================
@login_required
def generate_ai_summary(request, visit_id):
    visit = get_object_or_404(Visit, id=visit_id)

    # 🔒 Only doctor allowed
    if request.user.role != 'DOCTOR':
        return HttpResponseForbidden("Only doctors can generate AI summary")

    doctor = Doctor.objects.get(user=request.user)
    if visit.doctor != doctor:
        return HttpResponseForbidden("Not your visit")

    # Generate AI summary
    summary = generate_clinical_summary(visit)

    # Save summary safely
    visit.ai_summary = summary
    visit.save()

    return redirect('visit_context', visit_id=visit.id)
