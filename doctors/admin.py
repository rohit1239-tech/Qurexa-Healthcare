from django.contrib import admin
from .models import Doctor
from users.models import User


class DoctorAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user":
            kwargs["queryset"] = User.objects.filter(role="DOCTOR")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Doctor, DoctorAdmin)
