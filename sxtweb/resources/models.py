from django.db import models
from common.choices import *
import math
from django.utils.translation import ugettext_lazy as _

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
    LastModifiedByUser = models.CharField(max_length=32,verbose_name=_('Last Modified By User'))
    
    def __unicode__(self):
        return self.MachineName
    
    class Meta:
        verbose_name_plural = _("X-Ray Machines")
    
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

    def __unicode__(self):
        return '%s -- %s, %s %s, %d kV, %g mA' % (
            self.FilterCode,
            self.Machine.MachineCode,
            self.NominalHVL,
            self.HVLUnit,
            self.Energy,
            self.Current)
    
class CONE(models.Model):
    ConeCode = models.CharField(max_length=2, unique=True,verbose_name=_("Cone Code"))
    ConeName = models.CharField(max_length=64,unique=True,verbose_name=_("Cone Name"))
    Machine = models.ForeignKey(MACHINE, on_delete=models.CASCADE)
    Shape = models.CharField(max_length=32,
                             default="Circle",
                             choices=CONE_SHAPE_CHOICES,
                             verbose_name=_("Cone Shape"))
    Breadth = models.FloatField(verbose_name=_("Breadth (cm)"))
    Width = models.FloatField(verbose_name=_("Width (cm)"))
    FSD = models.FloatField(verbose_name="Focal Cone End Dist. (cm)")
    ConeEnd = models.CharField(max_length=32,choices=CONE_END_CHOICES,
                               default="Open",verbose_name="Cone End")
    Status = models.CharField(max_length=32, choices=HW_STATUS_CHOICES)    
    LastModifiedDateTime = models.DateTimeField(auto_now=True)
    LastModifiedByUser = models.CharField(max_length=32,verbose_name=_('Last Modified By User'))
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

class CHAMBER(models.Model):
    ChamberName = models.CharField(max_length=64,unique=True,verbose_name=_("Chamber Name"))
    ChamberModel = models.CharField(max_length=64,verbose_name=_("Chamber Model"))
    SerialNumber = models.CharField(max_length=64,unique=True,verbose_name=_("Serial Number"))
    LastModifiedDateTime = models.DateTimeField(auto_now=True)    
    LastModifiedByUser = models.CharField(max_length=32,verbose_name=_('Last Modified By User'))
    
    def __unicode__(self):
        return self.ChamberName

class ELECTROMETER(models.Model):
    ElectrometerName = models.CharField(max_length=64,unique=True,verbose_name=_("Electrometer Name"))
    ElectrometerModel = models.CharField(max_length=64,verbose_name=_("Electrometer Model"))
    SerialNumber = models.CharField(max_length=64,unique=True,verbose_name=_("Serial Number"))
    LastModifiedDateTime = models.DateTimeField(auto_now=True)    
    LastModifiedByUser = models.CharField(max_length=32,verbose_name=_('Last Modified By User'))
    
    def __unicode__(self):
        return self.ElectrometerName
    
class DOCTOR(models.Model):
    StaffId = models.CharField(max_length=16,unique=True,verbose_name=_('Staff ID'))
    LastName = models.CharField(max_length=64,verbose_name=_('Last Name'))
    FirstName = models.CharField(max_length=64,verbose_name=_('First Name'))
    LastModifiedDateTime = models.DateTimeField(auto_now=True)    
    
    def __unicode__(self):
        return '%s, %s' % (self.LastName, self.FirstName)

