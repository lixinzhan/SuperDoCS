from xcalc.models import *
from django.contrib import admin
from django import forms

class TreatmentPlanForm(forms.ModelForm):
    class Meta:
        model=TREATMENTPLAN
        # exclude = ['id']
        fields = '__all__'

class TreatmentPlanAdmin(admin.ModelAdmin):
    form = TreatmentPlanForm
    def Patient_Name(self, obj):
        return '{}, {}'.format(obj.LastName, obj.FirstName)
    def Prescription(self, obj):
        return '{0:g} / {1:d}'.format(obj.TotalDose, obj.Fractions)
    def Fraction_Dose(self, obj):
        return '{:g}'.format(obj.TotalDose/obj.Fractions)
    def Tx_Duration(self, obj):
        return '{:.1f}'.format(obj.TxTime)
    readonly_fields = [ f.name for f in TREATMENTPLAN._meta.get_fields()
                        if f.name!='id' ]
    list_display = ('PlanName','PatientId','Patient_Name',
                    'Prescription','Fraction_Dose','Tx_Duration')
    # exclude=['id']

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(TREATMENTPLAN,TreatmentPlanAdmin)
