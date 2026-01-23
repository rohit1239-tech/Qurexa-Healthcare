from django.contrib import admin
from django.urls import path, include
from .views import home

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('', include('users.urls')),   # ✅ REQUIRED
    path('appointments/', include('appointments.urls')),
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
    path('records/', include('records.urls')),
]
