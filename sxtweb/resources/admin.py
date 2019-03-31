# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import *


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
    list_display = ('ChamberName','ChamberModel','SerialNumber','Status')
admin.site.register(CHAMBER, ChamberAdmin)

class ElectrometerAdmin(admin.ModelAdmin):
    list_display = ('ElectrometerName','ElectrometerModel','SerialNumber','Status')
admin.site.register(ELECTROMETER,ElectrometerAdmin)

class DoctorAdmin(admin.ModelAdmin):
    def Full_Name(self,obj):
        return '{}, {} {}'.format(obj.LastName, obj.FirstName, obj.MiddleName)
    list_display = ('StaffId','Full_Name', 'Status')
admin.site.register(DOCTOR,DoctorAdmin)

