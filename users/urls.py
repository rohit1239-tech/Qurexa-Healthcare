from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    CustomLoginView,
    patient_signup,
    verify_otp,
    test_sendgrid_otp,   # ✅ NEW: temporary OTP test view
)

urlpatterns = [
    # 🔐 Authentication
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # 📝 Signup + OTP
    path('signup/', patient_signup, name='patient_signup'),
    path('verify-otp/', verify_otp, name='verify_otp'),

    # 🧪 TEMP: SendGrid OTP Test (remove later)
    path('test-sendgrid-otp/', test_sendgrid_otp, name='test_sendgrid_otp'),

    # 🔑 Forgot Password
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html'
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html'
        ),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html'
        ),
        name='password_reset_complete'
    ),
]
