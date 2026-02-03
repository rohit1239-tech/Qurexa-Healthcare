from django.urls import path
from .views import (
    patient_signup,
    send_otp,
    verify_otp,
    create_patient_account,
    patient_dashboard
)

urlpatterns = [
    path('signup/', patient_signup, name='patient_signup'),
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('create-account/', create_patient_account, name='create_patient_account'),
    path('dashboard/', patient_dashboard, name='patient_dashboard'),
]

