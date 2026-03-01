from django.contrib import admin
from authentication.models import DoctorProfile


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialization', 'is_approved')
    list_editable = ('is_approved',)

    def save_model(self, request, obj, form, change):

        #  When approved → activate user
        if obj.is_approved:
            obj.user.is_active = True
        else:
            obj.user.is_active = False

        obj.user.save()
        super().save_model(request, obj, form, change)


