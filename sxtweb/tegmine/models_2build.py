from django.db import models
from choices import *
from protocols.AAPM_TG61.Mu_WatAir_air import Mu_WatAir_air
from protocols.AAPM_TG61.BSF_Wat import BSF_Wat
from protocols.AAPM_TG61.BSF_CloseCone import BSF_CloseCone
import math
from django.utils.translation import ugettext_lazy as _

##########################################################################
#
# The real model difinations start from here.
#

class DOCTOR(models.Model):
    StaffId = models.CharField(max_length=16,unique=True,verbose_name=_('Staff ID'))
    LastName = models.CharField(max_length=64,verbose_name=_('Last Name'))
    FirstName = models.CharField(max_length=64,verbose_name=_('First Name'))
    LastModifiedDateTime = models.DateTimeField(auto_now=True)    
    
    def __unicode__(self):
        return '%s, %s' % (self.LastName, self.FirstName)

class MACHINE(models.Model):
    MachineCode = models.CharField(max_length=2, unique=True,verbose_name=_("Machine Code"))
    MachineName = models.CharField(max_length=64,unique=True,verbose_name=_("Machine Name"))
    MachineModel = models.CharField(max_length=64,verbose_name=_("Machine Model"))
    SerialNumber = models.CharField(max_length=64,unique=True,verbose_name=_("Serial Number"))
    Status = models.CharField(max_length=32, choices=HW_STATUS_CHOICES)    
    OutputControl = models.CharField(max_length=16, choices=OUTPUT_CONTROL_CHOICES,
                                     verbose_name=_("Output Control"))
    Description = models.TextField(max_length=512,blank=True)
    LastModifiedDateTime = models.DateTimeField(auto_now=True)    
    
    def __unicode__(self):
        return self.MachineName
    
    class Meta:
        verbose_name_plural = _("X-Ray Machines")
    
class CHAMBER(models.Model):
    ChamberName = models.CharField(max_length=64,unique=True,verbose_name=_("Chamber Name"))
    ChamberModel = models.CharField(max_length=64,verbose_name=_("Chamber Model"))
    SerialNumber = models.CharField(max_length=64,unique=True,verbose_name=_("Serial Number"))
    LastModifiedDateTime = models.DateTimeField(auto_now=True)    
    
    def __unicode__(self):
        return self.ChamberName

class ELECTROMETER(models.Model):
    ElectrometerName = models.CharField(max_length=64,unique=True,verbose_name=_("Electrometer Name"))
    ElectrometerModel = models.CharField(max_length=64,verbose_name=_("Electrometer Model"))
    SerialNumber = models.CharField(max_length=64,unique=True,verbose_name=_("Serial Number"))
    LastModifiedDateTime = models.DateTimeField(auto_now=True)    
    
    def __unicode__(self):
        return self.ElectrometerName
    
class MEASUREMENTSET(models.Model):
    Electrometer = models.ForeignKey(ELECTROMETER, on_delete=models.CASCADE)
    Chamber = models.ForeignKey(CHAMBER, on_delete=models.CASCADE)
    def __unicode__(self):
        return u'%s + %s' % (self.Electrometer.ElectrometerName, self.Chamber.ChamberName)
    class Meta:
        verbose_name_plural = "Measurement Sets"        

class FILTER(models.Model):
    FilterCode = models.CharField(max_length=2, unique=True,verbose_name=_("Filter Code"))
    FilterName = models.CharField(max_length=64,unique=True,verbose_name=_("Filter Name"))
    Machine = models.ForeignKey(MACHINE, on_delete=models.CASCADE)
    Energy = models.FloatField(verbose_name=_("Energy (kV)"))
    Current = models.FloatField(verbose_name=_("Current (mA)"))
    HVLUnit = models.CharField(max_length=16, default='mm Al',
                               choices=HVL_UNIT_CHOICES,verbose_name=_("HVL Unit"))
    NominalHVL = models.FloatField(verbose_name=_("Nominal HVL"))
    HVL = models.FloatField(verbose_name=_("Measured HVL"))
    EndEffect = models.FloatField(default=0.0,verbose_name=_("End Effect (min or MU)"))
    Status = models.CharField(max_length=32, choices=HW_STATUS_CHOICES)    
    LastModifiedDateTime = models.DateTimeField(auto_now=True)    
    LastModifiedByUser = models.CharField(max_length=32,verbose_name=_('Last Modified By User'))

    #def __unicode__(self):
    #    return '%s, %s (%s %s, %d kV)' % \
    #        (self.Machine.MachineName, self.FilterName, \
    #         self.NominalHVL, self.HVLUnit, self.Energy)
    def __unicode__(self):
        return '%s -- %s, %s %s, %d kV, %g mA' % (
            self.FilterCode,
            self.Machine.MachineCode,
            self.NominalHVL,
            self.HVLUnit,
            self.Energy,
            self.Current)
    
class CONE(models.Model):
    ConeCode = models.CharField(max_length=2, unique=True,verbose_name=_("Applicator Code"))
    ConeName = models.CharField(max_length=64,unique=True,verbose_name=_("Applicator Name"))
    Machine = models.ForeignKey(MACHINE, on_delete=models.CASCADE)
    Shape = models.CharField(max_length=32,
                             default="Circle",
                             choices=CONE_SHAPE_CHOICES,
                             verbose_name=_("Applicator Shape"))
    Breadth = models.FloatField(verbose_name=_("Breadth (cm)"))
    Width = models.FloatField(verbose_name=_("Width (cm)"))
    FSD = models.FloatField(verbose_name="Focal Applicator End Dist. (cm)")
    ConeEnd = models.CharField(max_length=32,choices=CONE_END_CHOICES,
                               default="Open",verbose_name="Applicator End")
    Status = models.CharField(max_length=32, choices=HW_STATUS_CHOICES)    
    LastModifiedDateTime = models.DateTimeField(auto_now=True)
    def getEquivDiameter(self):
        if self.Shape=='Circle':
            return self.Breadth
        elif self.Shape=='Square':
            return 2.0*self.Breadth/math.sqrt(math.pi)
        else: # rectangle
            return 4*self.Breadth*self.Width/(math.sqrt(math.pi)*(self.Breadth+self.Width))
        return -1
    def getEquivSquareLenth(self):
        if self.Shape=='Square':
            return self.Breadth
        elif self.Shape=='Circle':
            return math.sqrt(pi)*self.Breadth/2.0
        else: # rectangle
            return 2.0*self.Breadth*self.Width/(self.Breadth+self.Width)
        return -1
    def getMaxDimension(self):
        if self.Shape=='Square':
            return self.Breadth
        elif self.Shape=='Square':
            return self.Breadth*math.sqrt(2.0)
        else: #rectangle
            return math.sqrt(self.Breadth**2+self.Width**2)
        return -1
    #def __unicode__(self):
    #    return '%s, %s (FCD %d cm)' % (self.Machine.MachineName, self.ConeName, \
    #                                   self.FSD)
    def getConeShape(self):
        if self.Shape=='Circle':
            return 'Circ %d' % self.Breadth
        elif self.Shape=='Square':
            return '%dx%d'% (self.Breadth, self.Breadth)
        return '%dx%d' % (self.Breadth, self.Width)
        
    def __unicode__(self):
        return '%s -- %s, %s, FCD %d' % (
            self.ConeCode,
            self.Machine.MachineCode,
            self.getConeShape(),
            self.FSD)
    class Meta:
        verbose_name_plural = _("Applicators")

class CALIBRATION(models.Model):
    CalibName = models.CharField(max_length=32,unique=True,verbose_name=_('ID'))    
    Filter = models.ForeignKey(FILTER, on_delete=models.CASCADE)
    Cone = models.ForeignKey(CONE,verbose_name=_('Applicator'), on_delete=models.CASCADE)
    LocalStandard = models.ForeignKey(MEASUREMENTSET, related_name="%(app_label)s_%(class)s_LocalStandard",
                                      verbose_name=_('Local Standard Measurement Set'), on_delete=models.CASCADE)
    Nx = models.FloatField(default=0.0, blank=True, verbose_name=_("Nx (R/rdg)"))
    Nk = models.FloatField(default=0.0, verbose_name=_("Nk (cGy/rdg)"))
    MeasurementSet = models.ForeignKey(MEASUREMENTSET, related_name="%(app_label)s_%(class)s_MeasurementSet",
                                       verbose_name=_('Measurement Set'), on_delete=models.CASCADE)
    XcalFactor = models.FloatField(default=0.0) # cross calib factor against local std.
    Active = models.BooleanField(default=True)
    CalibrationMethod = models.CharField(max_length=32,
                                         default="in-Air",
                                         choices=CALIBRATION_METHOD_CHOICES,
                                         verbose_name=_('Calibration Method'))
    Pressure = models.FloatField(verbose_name=_("Pressure (mm Hg)"))
    Temperature = models.FloatField(verbose_name=_("Temperature (Celsius)"))    
    FDD = models.FloatField(verbose_name=_("Focal Detector Dist. (cm)"))
    IrradiationTime = models.FloatField(verbose_name=_("Beam Duration (min or MU)"))
    V_std = models.FloatField(default=300,verbose_name=_("Standard Voltage"))
    M_std = models.FloatField(verbose_name=_("Reading Average (for V_std)"))
    V_opp = models.FloatField(default=-300,verbose_name=_("Opposite Voltage"))
    M_opp = models.FloatField(verbose_name=_("Reading Average (for V_opp)"))
    V_low = models.FloatField(default=150,verbose_name=_("Low Voltage"))
    M_low = models.FloatField(verbose_name=_("Reading Average (for V_low)"))
            
    MeasurementDateTime = models.DateTimeField(verbose_name=_("Calib. Measurement"))
    MeasuredByUser = models.CharField(max_length=32,verbose_name=_('Measured By User'))
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
    BSF_ConeEnd = models.FloatField(default=0.0, verbose_name=_("BSF Correction Factor for Close-Ended Cone"))
    DR_Air = models.FloatField(default=0.0,verbose_name=_('Air Kerma Rate in Air'))
    DR_Water = models.FloatField(default=0.0,verbose_name=_('Dose Rate at Water Surface'))
    
    def save(self, *args, **kwargs):
        if not license_is_valid():
            return
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
        if not self.Nx:
            self.Nx = 0.0
        if (math.fabs(self.Nk)!=0.0): # if Nk is provided, use Nk.
            Kerma = Mcorr * self.XcalFactor * self.Nk * self.P_stem
        else: # otherwise, use Nx
            Kerma = Mcorr * self.XcalFactor * self.Nx * W_e * self.P_stem
        
        self.DR_Air = Kerma/(self.IrradiationTime - self.Filter.EndEffect)
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
    def __unicode__(self):
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
    
    def __unicode__(self):
        return 'ROF for %s with %s -- %s' %(self.Filter.Filter.FilterName,
                                            self.Cone.ConeName,
                                            self.ROFName)

    class Meta:
        verbose_name_plural = _("Output Factors")        


class TREATMENTPLAN(models.Model):
    PlanName = models.CharField(max_length=64)

    PatientId = models.CharField(max_length=16)
    LastName = models.CharField(max_length=64)
    FirstName = models.CharField(max_length=64)
    MiddleName = models.CharField(max_length=64)
    DOB = models.DateField()

    TotalDose = models.FloatField()
    Fractions = models.PositiveIntegerField()
    PrescriptionDepth = models.FloatField()
    TargetTissue = models.CharField(max_length=16,
                                    choices=MEDIUM_CHOICES)

    Filter = models.ForeignKey(CALIBRATION, #limit_choices_to={'Active':True},
                               verbose_name=_('Filter'), on_delete=models.CASCADE)
    Cone = models.ForeignKey(CONE,verbose_name=_('Applicator'), on_delete=models.CASCADE)
    CutoutRequired = models.BooleanField(default=False)
    CutoutShape = models.CharField(max_length=16, choices=SHAPE_CHOICES)
    CutoutLength = models.FloatField()
    CutoutWidth = models.FloatField()
    CutoutThickness = models.FloatField()
    StandOut = models.FloatField()

    FCD = models.FloatField(default=0)           # Focal Calib-Position Distance
    FSD = models.FloatField(default=0)           # Focal Surface Distance
    ISF = models.FloatField(default=0)           # Inverse Square Factor
    Dequiv = models.FloatField(default=0)        # Equivalent Diameter
    DequivCalib = models.FloatField(default=0)   # Equiv. Diameter at Calib. Position
    DequivSurface = models.FloatField(default=0) # Equiv. Diameter at Medium Surface

    SpecifyROF = models.BooleanField(default=False)
    ROF = models.FloatField(default=0)           # Relative Output Factor

    PDD = models.FloatField(default=100)           # Percentage Depth Dose

    KR_air_CalibCone = models.FloatField(default=0)  # Kerma Rate in Air for Calib. Pos.
    KR_air = models.FloatField(default=0)    # Kerma Rate in Air for Pt. Surface
    BSF_wat = models.FloatField(default=0)       # Back Scattering Factor for Water
    BSF_ConeEnd = models.FloatField(default=0)
    MassAbs_WatAir_air = models.FloatField(default=0)    # Mass Abs. Ratio
    DR_wat = models.FloatField(default=0)    # Dose Rate at Water Surface
    C_MedWat = models.FloatField(default=0)  # Mu_med_wat in air. See (Eq. 12) and Table X.
    B_MedWat = models.FloatField(default=0)  # Bmed/Bwat. Other than Bone, it is always ONE. See Table XI.
    DR_med = models.FloatField(default=0)    # Dose Rate at Medium Surface
    DosePerFrac = models.FloatField(default=0)   # Dose Per Fraction
    TxTime = models.FloatField(default=0)    # Treatment Time

    Doctor = models.ForeignKey(DOCTOR,verbose_name=_('Physician'), on_delete=models.CASCADE)
    Comment = models.TextField(max_length=512,blank=True)
    SXTCalcVersion = models.CharField(max_length=32)
    DoseCalibDate = models.DateField(null=True)
    ModifiedByUser = models.CharField(max_length=32)
    LastModifiedDateTime = models.DateTimeField(auto_now=True)
    
    PlanStatus = models.CharField(max_length=32,choices=PLAN_STATUS_CHOICES, default="Active")
    StatusChangedBy = models.CharField(max_length=32,blank=True)
    StatusChangeDateTime = models.DateTimeField(auto_now_add=True)
    ApprvStatus = models.CharField(max_length=32, choices=APPRV_STATUS_CHOICES,
                                   default="NotApproved")
    ApprovedBy = models.CharField(max_length=32, blank=True)
    ApprvDateTime = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return '%s (%s, %s): %d/%d, %s' % \
                (self.PlanName,
                 self.LastName,
                 self.FirstName,
                 self.TotalDose, self.Fractions,
                 self.TargetTissue)
    
    class Meta:
        verbose_name_plural = "Treatment Plans"        

##########################################################################
#
# Codes below are used for licensing issue.
#

def license_is_valid():    
    return True
