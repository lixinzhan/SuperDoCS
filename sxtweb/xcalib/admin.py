from django.contrib import admin

from .models import *

admin.site.register(LOCALSTANDARD)
admin.site.register(MEASUREMENTSET)

class OUTPUTFACTORAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['OutputFactorId', 'Filter', 'Cone', 'ConeFactor']}),
        ('Fitting Related', {'fields': ['DequivMax', 'DequivMin', 'CutoutThickness', 'FitMethod']}),
        ('Fitting Parameters for Sauver\'s Equation', {'fields': ['P','S','L','U','N']}),
        ('Parameters for Customized Curve Fitting', {'fields': ['A','B','C','D','E','F','G']}),
    ]
admin.site.register(OUTPUTFACTOR, OUTPUTFACTORAdmin)

class CALIBRATIONAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,  {'fields':['CalibrationId', 'Filter', 'Cone', 'CalibrationMethod','Status']}),
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

