from xcalc.models import *
from django.contrib import admin


class TreatmentPlanAdmin(admin.ModelAdmin):
    readonly_fields = [f.name for f in TREATMENTPLAN._meta.get_fields()]
    list_display = ('PlanName','PatientId','LastName','FirstName','MiddleName')
    #exclude=(['BSF_ConeEnd'])

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(TREATMENTPLAN,TreatmentPlanAdmin)
