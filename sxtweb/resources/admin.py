# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

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

class DoctorAdmin(admin.ModelAdmin):
    list_display = ('StaffId','LastName','FirstName')
admin.site.register(DOCTOR,DoctorAdmin)

