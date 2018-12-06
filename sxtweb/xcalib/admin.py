from django.contrib import admin
from django import forms

from protocols.TG61.HVLAlCu import HVLAlCu

from .models import *

admin.site.register(LOCALSTANDARD)



class MEASUREMENTSETForm(forms.ModelForm):
    class Meta:
        model = MEASUREMENTSET
        fields = '__all__'
    def clean_Filter(self):
        fltr = self.cleaned_data.get('Filter')
        lstd = self.cleaned_data.get('LocalStandard')

        if (fltr.HVLUnit==lstd.HVLUnit):
            tmphvl = fltr.HVL
        else:
            tmphvl = HVLAlCu.convertHVLUnit(fltr.HVL, fltr.HVLUnit)
        if math.fabs(1.0-lstd.HVL/tmphvl)>0.05:
            raise forms.ValidationError("%f Too much HVL difference for Filter and LocalStandard %f" 
                % (lstd.HVL, fltr.HVL))

        return self.cleaned_data['Filter']
 
class MEASUREMENTSETAdmin(admin.ModelAdmin):
     form = MEASUREMENTSETForm

admin.site.register(MEASUREMENTSET, MEASUREMENTSETAdmin)

class OUTPUTFACTORAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['ROFName', 'Filter', 'Cone', 'ConeFactor']}),
        ('Fitting Related', {'fields': ['DequivMax', 'DequivMin', 'CutoutThickness', 'FitMethod']}),
        ('Fitting Parameters for Sauver\'s Equation', {'fields': ['P','S','L','U','N']}),
        ('Parameters for Customized Curve Fitting', {'fields': ['A','B','C','D','E','F','G']}),
    ]
admin.site.register(OUTPUTFACTOR, OUTPUTFACTORAdmin)
# admin.site.register(OUTPUTFACTOR)

class CALIBRATIONAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields':['CalibName', 'Filter', 'Cone', 'CalibrationMethod','Status']}),
        ('Measurements', {'fields':['MeasurementSet','FDD','BeamDuration', 
        ('Pressure','Temperature'), 
        ('V_std', 'M_std'), ('V_opp', 'M_opp'), ('V_low', 'M_low'),
        'MeasurementDate', 'MeasuredByUser']}),
        ('Comments', {'fields': ['Comment']}),
        ('Results', {'fields': [('P_elec','P_stem','P_tp'),('P_pol','P_ion','P_isf'),
        ('MassAbs_WatAir_air','BSF_Wat','BSF_ConeEnd'),('DR_Air','DR_Water')]}),
    ]
    readonly_fields = ('P_elec','P_stem','P_tp','P_pol','P_ion','P_isf',
        'MassAbs_WatAir_air','BSF_Wat','BSF_ConeEnd','DR_Air','DR_Water')
admin.site.register(CALIBRATION, CALIBRATIONAdmin)

admin.site.register(NOMINALCALIBRATION)

