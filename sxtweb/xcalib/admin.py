from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _

from protocols.TG61.HVLAlCu import HVLAlCu

from .models import *

#########################################################
class LOCALSTANDARDAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['LocalStandardId', 'Status']}),
        ('Calibrated Set', {'fields': ['Electrometer', 'Chamber']}),
        ('Calibration Beam Quality', {'fields': ['HVL', 'HVLUnit']}), 
        ('Calibration Results', {'fields': ['Nk', 'Nx']}),
        ('Misc Information', {'fields': ['CalibratedBy', 'CalibrationDate','Comment']}),
    ]
    list_display = ('LocalStandardId', 'Electrometer', 'Chamber', 'HVL', 'HVLUnit', 'Nk', 'Status')
admin.site.register(LOCALSTANDARD, LOCALSTANDARDAdmin)

#########################################################
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
     fieldsets = [
         (None, {'fields': ['MSetName', 'Electrometer', 'Chamber', 'Status']}),
         ('Calibrate Against', {'fields': ['LocalStandard']}),
         ('Setup for X-Calib.', {'fields': ['Filter', 'Cone']}),
         ('Measurements', {'fields': ['M_LS', 'M_MS']}),
         ('Misc Information', {'fields': ['CalibratedByUser', 'CalibrationDate', 'Comment']}),
         ('Results', {'fields': ['XCalFactor', 'Nk', 'Nx']}),
     ]
     def Cross_Calib_Factor(self, obj):
         return "%.3f" % obj.XCalFactor
     def Nk_Calibd(self, obj):
         return "%.3f" % obj.Nk
     readonly_fields = ('XCalFactor', 'Nk', 'Nx')
     list_display = ('MSetName', 'Electrometer', 'Chamber', 'Filter', 'Cross_Calib_Factor', 'Nk_Calibd', 'Status')

admin.site.register(MEASUREMENTSET, MEASUREMENTSETAdmin)

#########################################################
class OUTPUTFACTORAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['ROFName', 'Filter', 'Cone', 'ConeFactor']}),
        ('Fitting Related', {'fields': ['DequivMax', 'DequivMin', 'CutoutThickness', 'FitMethod']}),
        ('Fitting Parameters for Builtin Fitting Options', {'fields': ['P','S','U','L','N']}),
        ('Parameters for Customized Curve Fitting', {'fields': ['A','B','C','D','E','F','G']}),
    ]
    list_display = ('ROFName', 'Filter', 'Cone', 'ConeFactor', 'FitMethod')
admin.site.register(OUTPUTFACTOR, OUTPUTFACTORAdmin)

#########################################################
class CALIBRATIONForm(forms.ModelForm):
    class Meta:
        model = CALIBRATION
        fields = '__all__'
    #def __init__(self, *args, **kwargs):
    #    super().__init__(*args, **kwargs)
    #    try:
    #        self.dr_unit = 'cGy/' + self.instance.Filter.Machine.OutputControl
    #    except:
    #        self.dr_unit = 'cGy/MU or cGy/min'
    #    self.fields['DR_Air'].label = _('Air Kerma Rate in Air') + ' (' + self.dr_unit+')'
    #    self.fields['DR_Water'].label = _('Dose Rate at Water Surface') + ' (' + self.dr_unit + ')'

class CALIBRATIONAdmin(admin.ModelAdmin):
    form = CALIBRATIONForm
    fieldsets = [
        (None,  {'fields':['CalibName', 'Filter', 'Cone', 
        'CalibrationMethod','Status']}),
        ('Measurements', {'fields':['MeasurementSet', 
        ('P_elec', 'P_stem'),
        ('FDD','P_isf'), 
        ('BeamDuration','DurationUnit'), 
        ('Pressure','Temperature', 'P_tp'), 
        'Has_Pion_Ppol',
        ('V_std', 'M_std'), ('V_opp', 'M_opp'), ('V_low', 'M_low'),
        ('P_pol','P_ion'),
        ('MeasurementDate', 'MeasuredByUser')
        ]}),
        ('Intermediate values', {'fields': [
        ('MassAbs_WatAir_air','BSF_Wat','BSF_ConeEnd')]}),
        ('Calibration Results', {'fields': ['DR_Air','DR_Water']}),
        ('Comments', {'fields': ['Comment']}),
    ]
    readonly_fields = ('MassAbs_WatAir_air','BSF_Wat','BSF_ConeEnd') 
    formfield_overrides = {
        models.TextField: {'widget':forms.Textarea (attrs={'rows':3,'cols':80})},
    }

    def Air_Kerma_Rate(self, obj):
        return "%.3f" % obj.DR_Air
    def Dose_Rate_in_Water(self, obj):
        return "%.3f" % obj.DR_Water
    list_display = ('CalibName', 'Filter', 'Cone', 'Status', 
                    'Air_Kerma_Rate', 'Dose_Rate_in_Water', 'Status')
    class Media:
        js = (
            'admin/js/jquery.min.js',
            'admin/js/dyn_calib.js',
            )
admin.site.register(CALIBRATION, CALIBRATIONAdmin)


#########################################################
class NOMINALCALIBRATIONForm(forms.ModelForm):
    class Meta:
        model = NOMINALCALIBRATION
        exclude = ['DR_Water']
        # fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            self.dr_unit = 'cGy/' + self.instance.Filter.Machine.OutputControl
        except:
            self.dr_unit = 'cGy/MU or cGy/min'
        self.fields['DR_Air'].label = _('Air Kerma Rate in Air') + ' (' + self.dr_unit+')'
        # self.fields['DR_Water'].label = _('Dose Rate at Water Surface') + ' (' + self.dr_unit + ')'

class NOMINALCALIBRATIONAdmin(admin.ModelAdmin):
    form = NOMINALCALIBRATIONForm
    def Air_Kerma_Rate(self, obj):
        return "%.3f" % obj.DR_Air
    list_display = ('NCalibName', 'Filter', 'Cone', 'Status', 'Air_Kerma_Rate', 'Status')

admin.site.register(NOMINALCALIBRATION, NOMINALCALIBRATIONAdmin)

