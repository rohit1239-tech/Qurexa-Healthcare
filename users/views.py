import random

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from .forms import PatientSignupForm
from .models import OTP, User
from patients.models import Patient





class CustomLoginView(LoginView):
    template_name = 'login.html'

    def get_success_url(self):
        user = self.request.user

        if user.role == 'ADMIN':
            return reverse_lazy('admin:index')   # ✅ Django admin

        if user.role == 'DOCTOR':
            return reverse_lazy('doctor_dashboard')

        if user.role == 'PATIENT':
            return reverse_lazy('patient_dashboard')

        return reverse_lazy('home')



    def get_success_url(self):
        user = self.request.user

        if user.role == 'ADMIN':
            return reverse_lazy('admin:index')

        if user.role == 'DOCTOR':
            return reverse_lazy('doctor_dashboard')

        if user.role == 'PATIENT':
            return reverse_lazy('patient_dashboard')

        return reverse_lazy('home')


# ---------------------------
# PATIENT SIGNUP (SEND OTP)
# ---------------------------
def patient_signup(request):
    if request.method == 'POST':
        form = PatientSignupForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            contact = form.cleaned_data['contact']

            # prevent duplicate usernames
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already exists")
                return redirect('patient_signup')

            otp_code = str(random.randint(100000, 999999))

            # clear old OTPs
            OTP.objects.filter(contact=contact, purpose='SIGNUP').delete()

            OTP.objects.create(
                contact=contact,
                otp=otp_code,
                purpose='SIGNUP'
            )

            # TEMP: console log (later email/SMS)
            print("OTP for", contact, "is", otp_code)

            request.session['signup_username'] = username
            request.session['signup_contact'] = contact

            messages.success(request, "OTP sent successfully")
            return redirect('verify_otp')

    else:
        form = PatientSignupForm()

    return render(request, 'users/signup.html', {'form': form})


# ---------------------------
# VERIFY OTP + CREATE ACCOUNT
# ---------------------------
def verify_otp(request):
    contact = request.session.get('signup_contact')
    username = request.session.get('signup_username')

    if not contact or not username:
        return redirect('patient_signup')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        password = request.POST.get('password')

        try:
            otp_obj = OTP.objects.get(
                contact=contact,
                otp=entered_otp,
                purpose='SIGNUP'
            )
        except OTP.DoesNotExist:
            return render(request, 'users/verify_otp.html', {
                'error': 'Invalid OTP'
            })

        # create user safely
        user = User.objects.create(
            username=username,
            role='PATIENT',
            mobile=contact if contact.isdigit() else None,
            email=contact if '@' in contact else ''
        )
        user.set_password(password)   # ✅ CORRECT WAY
        user.save()

        # create patient profile
        Patient.objects.create(user=user)

        # cleanup
        otp_obj.delete()
        request.session.flush()

        # auto login
        login(request, user)

        return redirect('patient_dashboard')

    return render(request, 'users/verify_otp.html')
