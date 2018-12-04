from tegmine.models import *
from django.contrib import admin


class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ('PlanName','PatientId','LastName','FirstName','MiddleName')
    #exclude=(['BSF_ConeEnd'])
admin.site.register(TREATMENTPLAN,TreatmentPlanAdmin)
