import random
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.utils.timezone import now

from appointments.models import Appointment
from records.models import Visit
from patients.models import Patient

User = get_user_model()



# ============================
# PATIENT SIGNUP (EMAIL OTP)
# ============================

def patient_signup(request):
    return render(request, 'patients/signup.html')


def send_otp(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')

        if not email or not username:
            messages.error(request, 'Email and username are required')
            return redirect('patient_signup')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('patient_signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return redirect('patient_signup')

        otp = random.randint(100000, 999999)

        request.session['otp'] = str(otp)
        request.session['email'] = email
        request.session['username'] = username

        try:
            send_mail(
                subject='Your Qurexa OTP',
                message=f'Your OTP is {otp}',
                from_email=None,   # uses EMAIL_HOST_USER
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            print("EMAIL ERROR:", e)
            messages.error(request, 'Failed to send OTP. Email service error.')
            return redirect('patient_signup')

        messages.success(request, 'OTP sent to your email')
        return redirect('verify_otp')

    return redirect('patient_signup')


def verify_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')

        if entered_otp == session_otp:
            return redirect('create_patient_account')
        else:
            messages.error(request, 'Invalid OTP')
            return redirect('verify_otp')

    return render(request, 'patients/verify_otp.html')


def create_patient_account(request):
    email = request.session.get('email')
    username = request.session.get('username')

    if not email or not username:
        messages.error(request, 'Session expired. Please signup again.')
        return redirect('patient_signup')

    # create user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=User.objects.make_random_password()
    )

    # create patient profile
    Patient.objects.create(user=user)

    # cleanup session
    request.session.flush()

    messages.success(request, 'Account created successfully. Please login.')
    return redirect('login')


# ============================
# PATIENT DASHBOARD (UNCHANGED LOGIC)
# ============================

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

