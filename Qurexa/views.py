from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
import random
def home(request):
    return render(request, 'home.html')

def test_email(request):
    send_mail(
        subject='Qurexa SMTP Test',
        message='If you received this email, SMTP is working on PythonAnywhere.',
        from_email=None, # Uses DEFAULT_FROM_EMAIL
        recipient_list=['yengantiwarrohit1239@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("✅ Email sent successfully")


def test_otp_view(request):
    otp = random.randint(100000, 999999)

    # TEMP: show OTP directly on browser
    return HttpResponse(f"Generated OTP is: {otp}")
