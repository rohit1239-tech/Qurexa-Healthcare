from django.contrib import admin
from .models import Visit


class VisitAdmin(admin.ModelAdmin):
    readonly_fields = ('patient', 'doctor', 'created_at')
    list_display = ('patient', 'doctor', 'created_at')
    ordering = ('-created_at',)


admin.site.register(Visit, VisitAdmin)
