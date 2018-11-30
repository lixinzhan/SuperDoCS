from django.contrib import admin

from django.contrib import admin

from .models import *

class TREATMENTPLANAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Patient Information', {'fields': ['PatientId', 'LastName', 'FirstName', 
            'MiddleName','DOB']}),
        ('Prescription', {'fields': ['TotalDose', 'Fractions', 
            'PrescriptionDepth', 'TargetTissue']}),
        ('Plan Setup', {'fields':['Filter','Cone','CutoutRequired',
            'CutoutShape','CutoutLength','CutoutWidth','CutoutThickness','StandOut']}),
    ]
admin.site.register(TREATMENTPLAN, TREATMENTPLANAdmin)
