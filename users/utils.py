import random
from django.core.mail import send_mail

def send_otp_email(email):
    otp = random.randint(100000, 999999)

    try:
        send_mail(
            subject="Qurexa Account Verification OTP",
            message=f"Your OTP is {otp}. It is valid for 5 minutes.",
            from_email=None,   # uses DEFAULT_FROM_EMAIL
            recipient_list=[email],
            fail_silently=False,
        )
        return otp

    except Exception as e:
        print("EMAIL ERROR:", e)   # 👈 shows real error in logs
        return None
