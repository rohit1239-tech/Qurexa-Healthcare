from django.contrib import admin
from .models import Patient
from users.models import User


class PatientAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role="PATIENT")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Patient, PatientAdmin)
