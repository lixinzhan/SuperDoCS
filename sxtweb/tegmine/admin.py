from tegmine.models import *
from django.contrib import admin

class MachineAdmin(admin.ModelAdmin):
    list_display = ('MachineCode','MachineName','MachineModel','SerialNumber','Status')
admin.site.register(MACHINE, MachineAdmin)

class FilterAdmin(admin.ModelAdmin):
    list_display = ('FilterCode','FilterName','Machine','Energy','Current','NominalHVL', 'HVLUnit','Status')
    # exclude = ('EndEffect',)
admin.site.register(FILTER, FilterAdmin)

class ConeAdmin(admin.ModelAdmin):
    list_display = ('ConeCode','ConeName', 'Machine','Shape','Breadth','Width','FSD','Status')
    #exclude=(['ConeEnd'])
admin.site.register(CONE,ConeAdmin)

class ChamberAdmin(admin.ModelAdmin):
    list_display = ('ChamberName','ChamberModel','SerialNumber')
admin.site.register(CHAMBER, ChamberAdmin)

class ElectrometerAdmin(admin.ModelAdmin):
    list_display = ('ElectrometerName','ElectrometerModel','SerialNumber')
admin.site.register(ELECTROMETER,ElectrometerAdmin)

admin.site.register(MEASUREMENTSET)

class CalibrationAdmin(admin.ModelAdmin):
    list_display = ('CalibName','Filter','Cone','CalibrationMethod','DR_Air','MeasurementDateTime','Active')
    # date_hierarchy = 'MeasurementDateTime'
    fieldsets = [
        (None, {'fields': ['CalibName','Filter','Cone','LocalStandard',
                           'Nx','Nk','MeasurementSet','XcalFactor','Active',
                           'CalibrationMethod','Pressure','Temperature','FDD','IrradiationTime','P_stem',
                           'V_std','M_std','V_opp','M_opp','V_low','M_low','MeasurementDateTime',
                           'MeasuredByUser','LastModifiedByUser','Comment']}),
        ('Calibration Result Review (For QA purpose only)',
                {'fields': ['P_tp','P_pol','P_ion','P_isf','MassAbs_WatAir_air',
                            'BSF_Wat','DR_Air','DR_Water'], 'classes': ['collapse']})
    ]
    #exclude=('P_elec', 'P_stem', 'P_tp', 'P_pol', 'P_ion', 'P_isf',
    #         'MassAbs_WatAir_air', 'BSF_Wat', 'DR_Air', 'DR_Water')
admin.site.register(CALIBRATION, CalibrationAdmin)

class OutputFactorAdmin(admin.ModelAdmin):
    list_display = ('ROFName','Filter','Cone')
admin.site.register(OUTPUTFACTOR,OutputFactorAdmin)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('StaffId','LastName','FirstName')
admin.site.register(DOCTOR,DoctorAdmin)

class TreatmentPlanAdmin(admin.ModelAdmin):
    list_display = ('PlanName','PatientId','LastName','FirstName','MiddleName')
    #exclude=(['BSF_ConeEnd'])
admin.site.register(TREATMENTPLAN,TreatmentPlanAdmin)
