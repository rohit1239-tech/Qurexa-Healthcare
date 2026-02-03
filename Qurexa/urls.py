from django.contrib import admin
from django.urls import path, include
from .views import home
from django.urls import path
from . import views
from .views import test_otp_view

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),   # ✅ REQUIRED
    path('appointments/', include('appointments.urls')),
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
    path('records/', include('records.urls')),
    path('test-email/', views.test_email, name='test_email'),
    path('test-otp/', test_otp_view, name='test_otp'),
]
