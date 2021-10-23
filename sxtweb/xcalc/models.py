from django.db import models
from django.utils.translation import gettext_lazy as _

import math

from protocols.TG61.Mu_WatAir_air import Mu_WatAir_air
from protocols.TG61.BSF_Wat import BSF_Wat
from protocols.TG61.BSF_CloseCone import BSF_CloseCone

from common.choices import *
from resources.models import *
from xcalib.models import *

##########################################################################
#
# The real model difinations start from here.
#

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

    Filter = models.ForeignKey(NOMINALCALIBRATION, #limit_choices_to={'Active':True},
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
    ROF_Exposure = models.FloatField(default=0)           # Relative Output Factor

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
    
    def __str__(self):
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
