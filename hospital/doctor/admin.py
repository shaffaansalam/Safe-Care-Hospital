from django.contrib import admin
from authentication.models import DoctorProfile

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'is_approved')
    list_editable = ('is_approved',)

    def save_model(self, request, obj, form, change):
        if obj.is_approved:
            obj.user.is_active = True   #  Activate user on approval
            obj.user.save()
        super().save_model(request, obj, form, change)


