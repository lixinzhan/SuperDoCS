# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

import math

from protocols.TG61.Mu_WatAir_air import Mu_WatAir_air
from protocols.TG61.BSF_Wat import BSF_Wat
from protocols.TG61.BSF_CloseCone import BSF_CloseCone

from common.choices import *
from resources.models import *

class LOCALSTANDARD(models.Model):
    LocalStandardId = models.CharField(max_length=32,unique=True,verbose_name=_('Local Standard ID'))    
    Electrometer = models.ForeignKey(ELECTROMETER, on_delete=models.CASCADE)
    Chamber = models.ForeignKey(CHAMBER, on_delete=models.CASCADE)
    HVLUnit = models.CharField(max_length=16, default='mm Al',
                               choices=HVL_UNIT_CHOICES,verbose_name=_("HVL Unit"))
    HVL = models.FloatField(verbose_name=_("Calibration HVL"))
    Nx = models.FloatField(default=0.0, blank=True, verbose_name=_("Nx (R/rdg)"))
    Nk = models.FloatField(default=0.0, verbose_name=_("Nk (cGy/rdg)"))
    Status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    CalibrationDate = models.DateField()
    CalibratedBy = models.CharField(max_length=32, verbose_name=_("Calibrated By"), choices=CALIB_INST_CHOICES)
    Comment = models.TextField(max_length=256,blank=True)    

    def __str__(self):
        return '%s' % (self.LocalStandardId)
    class Meta:
        verbose_name_plural = "Local Standards"        

class MEASUREMENTSET(models.Model):
    MSetName = models.CharField(max_length=32, verbose_name=_("Meas Set Name"))
    Electrometer = models.ForeignKey(ELECTROMETER, on_delete=models.CASCADE)
    Chamber = models.ForeignKey(CHAMBER, on_delete=models.CASCADE)
    LocalStandard = models.ForeignKey(LOCALSTANDARD, on_delete=models.CASCADE)
    Filter = models.ForeignKey(FILTER, on_delete=models.CASCADE)
    Cone = models.ForeignKey(CONE,verbose_name=_('Applicator'), on_delete=models.CASCADE)
    M_LS = models.FloatField(default=0.0, verbose_name=_("Local Std Rdg"))
    M_MS = models.FloatField(default=0.0, verbose_name=_("Current Set Rdg"))
    XCalFactor = models.FloatField(default=0.0) # cross calib factor against local std.
    Nx = models.FloatField(default=0.0, blank=True, verbose_name=_("Nx (R/rdg)"))
    Nk = models.FloatField(default=0.0, blank=True, verbose_name=_("Nk (cGy/rdg)"))
    Status = models.CharField(max_length=32, choices=STATUS_CHOICES)
    CalibrationDate = models.DateField()
    CalibratedByUser = models.CharField(max_length=32)
    Comment = models.TextField(max_length=256,blank=True)    

    def save(self, *args, **kwargs):
        # if self.LocalStandard.HVLUnit==self.Filter.HVLUnit:
        #     tmphvl = self.Filter.HVL
        # else:
        #     tmphvl = HVLAlCu.convertHVLUnit(self.Filter.HVL, self.Filter.HVLUnit)
        # if math.fabs(1.0-self.LocalStandard.HVL/tmphvl)>0.05:
        #     self.Note='too much differece in HVL'
        self.XCalFactor = self.M_LS/self.M_MS
        self.Nx = self.LocalStandard.Nx * self.XCalFactor
        self.Nk = self.LocalStandard.Nk * self.XCalFactor
        super(MEASUREMENTSET,self).save(*args, **kwargs) # Call the "real" save() method.

    def __str__(self):
        return '%s: %s + %s' % (self.MSetName, self.Electrometer.ElectrometerName, self.Chamber.ChamberName)

    class Meta:
        verbose_name_plural = "Measurement Sets"        

class CALIBRATION(models.Model):
    CalibName = models.CharField(max_length=32,unique=True,verbose_name=_('ID'))    
    Filter = models.ForeignKey(FILTER, on_delete=models.CASCADE)
    Cone = models.ForeignKey(CONE,verbose_name=_('Applicator'), on_delete=models.CASCADE)
    CalibrationMethod = models.CharField(max_length=32,
                                         default="in-Air",
                                         choices=CALIBRATION_METHOD_CHOICES,
                                         verbose_name=_('Calibration Method'))
    Status = models.CharField(max_length=16, default="Active",choices=STATUS_CHOICES)
    MeasurementSet = models.ForeignKey(MEASUREMENTSET, related_name="%(app_label)s_%(class)s_MeasurementSet",
                                       verbose_name=_('Measurement Set'), on_delete=models.CASCADE)
    FDD = models.FloatField(verbose_name=_("Focal Detector Dist. (cm)"))
    Pressure = models.FloatField(verbose_name=_("Pressure (mm Hg)"))
    Temperature = models.FloatField(verbose_name=_("Temperature (Celsius)"))    
    BeamDuration = models.FloatField(verbose_name=_("Beam Duration (min or MU)"))

    V_std = models.FloatField(default=300,verbose_name=_("Standard Voltage"))
    M_std = models.FloatField(verbose_name=_("Reading Average (for V_std)"))
    V_opp = models.FloatField(default=-300,verbose_name=_("Opposite Voltage"))
    M_opp = models.FloatField(verbose_name=_("Reading Average (for V_opp)"))
    V_low = models.FloatField(default=150,verbose_name=_("Low Voltage"))
    M_low = models.FloatField(verbose_name=_("Reading Average (for V_low)"))
            
    MeasurementDate = models.DateField(verbose_name=_("Measured On"))
    MeasuredByUser = models.CharField(max_length=32,verbose_name=_('Measured By'))
    LastModifiedDateTime = models.DateTimeField(auto_now=True)
    LastModifiedByUser = models.CharField(max_length=32,
                                          verbose_name=_('Last Modified By User')) # default to current user in views.py
    Comment = models.TextField(max_length=512,blank=True)    
    
    P_elec = models.FloatField(default=1.0) # 1.0 if Electrometer-Chamber Calibrated together
    P_stem = models.FloatField(default=1.0,verbose_name=_('Stem Factor')) # 1.0 by default for stem correction
    P_tp = models.FloatField(default=0.0)
    P_pol = models.FloatField(default=0.0)
    P_ion = models.FloatField(default=0.0)
    P_isf = models.FloatField(default=0.0)

    MassAbs_WatAir_air = models.FloatField(default=0.0,verbose_name=_("Mass Abs. Coeff. (Water to Air in Air)"))
    BSF_Wat = models.FloatField(default=0.0, verbose_name=_("Back Scattering Factor for Water"))
    BSF_ConeEnd = models.FloatField(default=0.0, 
                                verbose_name=_("BSF Correction Factor for Close-Ended Cone"))
    DR_Air = models.FloatField(default=0.0,blank=True,
                                verbose_name=_('Air Kerma Rate in Air'))
    DR_Water = models.FloatField(default=0.0,blank=True,
                                verbose_name=_('Dose Rate at Water Surface'))
    
    def save(self, *args, **kwargs):
        self.P_tp = 760.0 * (self.Temperature+273.2)/(self.Pressure*295.2)
        self.P_isf = (self.FDD/self.Cone.FSD)**2
        
        mp = math.fabs(self.M_std)
        mn = math.fabs(self.M_opp)
        self.P_pol = (mp+mn)/(2.0*mp)
        
        mh = math.fabs(self.M_std)
        ml = math.fabs(self.M_low)
        vh = math.fabs(self.V_std)
        vl = math.fabs(self.V_low)
        mhl = (mh+0.0)/ml
        vhl = (vh+0.0)/vl
        self.P_ion = (1-vhl**2)/(mhl-vhl**2)
        
        mu = Mu_WatAir_air()
        self.MassAbs_WatAir_air = mu.getValue(self.Filter.HVLUnit,
                                              self.Filter.HVL)
        
        bsf = BSF_Wat()
        self.BSF_Wat = bsf.getValue(self.Cone.FSD,
                        self.Cone.getEquivDiameter(),
                        self.Filter.HVL,
                        self.Filter.HVLUnit)
        if self.Cone.ConeEnd=='PMMA3p2':
            bsfcc = BSF_CloseCone()
            self.BSF_ConeEnd = bsfcc.getValue(self.Cone.getEquivDiameter(),
                                            self.Filter.HVL,
                                            self.Filter.HVLUnit)
        elif self.Cone.ConeEnd=="Open":
            self.BSF_ConeEnd = 1.0
        else:
            self.BSF_ConeEnd = 0.0  # just in case of wrong cone-end type.
            
        Mcorr = math.fabs(self.M_std) * self.P_isf * self.P_tp * self.P_pol * \
                self.P_ion * self.P_elec
        W_e = 0.876  # (W/e)_air: 0.00876 Gy/R. Here we use 0.876 cGy/R
        # if not self.Nx:
        #     self.Nx = 0.0
        if (math.fabs(self.MeasurementSet.Nk)!=0.0): # if Nk is provided, use Nk.
            Kerma = Mcorr * self.MeasurementSet.Nk * self.P_stem
        else: # otherwise, use Nx
            Kerma = Mcorr * self.MeasurementSet.Nx * W_e * self.P_stem
        
        self.DR_Air = Kerma/(self.BeamDuration - self.Filter.EndEffect)
        self.DR_Water = self.DR_Air*self.MassAbs_WatAir_air*self.BSF_Wat*self.BSF_ConeEnd
        
        super(CALIBRATION, self).save(*args, **kwargs) # Call the "real" save() method.
        
    #def __unicode__(self):
    #    return u'%s, %s (%s %s, %s kV, C\'d %s) -- %s' % (
    #                                self.Filter.Machine.MachineName,
    #                                self.Filter.FilterName,
    #                                self.Filter.NominalHVL, self.Filter.HVLUnit,
    #                                self.Filter.Energy,
    #                                str(self.MeasurementDateTime,)[:10],
    #                                self.CalibName)
    def __str__(self):
        return u'%s -- %s, %s %s, %d kV, %g mA (%s)' % (
            self.Filter.FilterCode,
            self.Filter.Machine.MachineCode,
            self.Filter.NominalHVL, self.Filter.HVLUnit,
            self.Filter.Energy,
            self.Filter.Current,
            #str(self.MeasurementDateTime,)[:10],
            #self.CalibName,
            self.Cone.getConeShape(),
        )

    #class Admin:
    #    list_display=('Filter','Cone','MeasurementSet','Active','CalibrationMethod',
    #                  'Pressure','Temperature','FDD','IrradiationTime',
    #                  'V_std','M_std','V_opp','M_opp','V_low','M_low',
    #                  'MeasurementDateTime','MeasuredByUser','LastModifiedByUser',
    #                  'Comment')


class OUTPUTFACTOR(models.Model):
    ROFName = models.CharField(max_length=32, unique=True, verbose_name=_('ID'))    
    Filter = models.ForeignKey(CALIBRATION, verbose_name=_('Calib\'d Filter'), on_delete=models.CASCADE)
    Cone = models.ForeignKey(CONE,verbose_name=_('Applicator'), on_delete=models.CASCADE)
    FitMethod = models.CharField(max_length=32, choices=CURVE_FITTING_CHOICES,
                                 verbose_name=_('Curve Fitting Method'))
    ConeFactor = models.FloatField(default=0,verbose_name=_('Cone Factor'))
    DequivMax = models.FloatField(default=0, verbose_name=_("Max Allowed Equiv. Diameter (cm)"))
    DequivMin = models.FloatField(default=0, verbose_name=_("Min Allowed Equiv. Diameter (cm)"))
    CutoutThickness = models.FloatField(default=0.2, verbose_name=_("Cutout Thickness (cm)"))

    # Fitting parameters for Sauver's eqn, the default
    P = models.FloatField(default=0)
    S = models.FloatField(default=0)
    L = models.FloatField(default=0)
    U = models.FloatField(default=0)
    N = models.FloatField(default=0)

    # Extra fitting parameters for customized curve fitting
    A = models.FloatField(default=0)
    B = models.FloatField(default=0)
    C = models.FloatField(default=0)
    D = models.FloatField(default=0)
    E = models.FloatField(default=0)
    F = models.FloatField(default=0)
    G = models.FloatField(default=0)
    
    def __str__(self):
        return 'ROF for %s with %s -- %s' %(self.Filter.Filter.FilterName,
                                            self.Cone.ConeName,
                                            self.ROFName)

    class Meta:
        verbose_name_plural = _("Output Factors")        

class NOMINALCALIBRATION(models.Model):
    NCalibName = models.CharField(max_length=32,unique=True,verbose_name=_('Nominal Calib. Name'))    
    Filter = models.ForeignKey(FILTER, on_delete=models.CASCADE)
    Cone = models.ForeignKey(CONE, on_delete=models.CASCADE)
    Status = models.CharField(max_length=16, default="Active",choices=STATUS_CHOICES)
    DR_Air = models.FloatField(default=0.0,verbose_name=_('Air Kerma Rate in Air (cGy/MU or cGy/min)'))
    DR_Water = models.FloatField(default=0.0,verbose_name=_('Dose Rate at Water Surface (cGy/MU or cGy/min)'))
    LastModifiedDateTime = models.DateTimeField(auto_now=True)
    LastModifiedByUser = models.CharField(max_length=32,
                                          verbose_name=_('Last Modified By User')) # default to current user in views.py
    Comment = models.TextField(max_length=512,blank=True)   

    def __str__(self):
        return '%s: %.2f' % (self.NCalibName, self.DR_Air)

    class Meta:
        verbose_name = _('Nominal Calibration')


