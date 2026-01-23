from django.urls import path
from .views import (
    book_appointment,
    doctor_appointments,
    update_appointment_status,
    complete_appointment
)

urlpatterns = [
    path('book/', book_appointment, name='book_appointment'),
    path('doctor/', doctor_appointments, name='doctor_appointments'),
    path('update/<int:pk>/', update_appointment_status, name='update_appointment_status'),
    path('complete/<int:appointment_id>/', complete_appointment, name='complete_appointment'),
]
