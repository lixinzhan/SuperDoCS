from django import forms
import datetime
import numpy as np
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from common.choices import *
from .models import *
from xcalib.models import *

class AuthForm(forms.Form):
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(label=_("Password"),widget=forms.PasswordInput)
    def __init__(self, user, *args, **kwargs):
        self.authuser = user
        super(AuthForm, self).__init__(*args, **kwargs)        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            self.authuser = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(_('User Dose Not Exist!'))
        if self.authuser.groups.filter(name='Physicists').count()==0:
            raise forms.ValidationError(_('You are not a Physicist!'))
        return username
    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            username = self.cleaned_data['username']
            self.authuser = User.objects.get(username=username)
        except:
            raise forms.ValidationError(_('Username and Password Not Match!'))
            
        try:
            if not self.authuser.check_password(password):
                raise forms.ValidationError(_('Incorrect Password, Try Again!'))
        except User.DoesNotExist:
            raise forms.ValidationError(_('User Dose Not Exist!'))
        return password
    
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['last_name', 'first_name', 'email']

class PasswordForm(forms.Form):
    oldpasswd = forms.CharField(label=_("Old Password"), widget=forms.PasswordInput)
    newpasswd = forms.CharField(label=_("New Password"), widget=forms.PasswordInput)
    checkpasswd = forms.CharField(label=_("Password Again"), widget=forms.PasswordInput)
    
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(PasswordForm, self).__init__(*args, **kwargs)        
    def clean_oldpasswd(self):
        oldpasswd = self.cleaned_data['oldpasswd']
        if not self.user.check_password(oldpasswd):
            raise forms.ValidationError('Incorrect Password!')
        return oldpasswd
    def clean_newpasswd(self):
        newpasswd = self.cleaned_data['newpasswd']
        if len(newpasswd)<6:
            raise forms.ValidationError('Password too short!')
        return newpasswd
    def clean_checkpasswd(self):
        newpasswd = self.cleaned_data.get('newpasswd','')
        checkpasswd = self.cleaned_data['checkpasswd']
        if len(checkpasswd)<6:
            raise forms.ValidationError('Password too short!')            
        if newpasswd != checkpasswd:
            raise forms.ValidationError('Password Fields NOT Match!')
        return checkpasswd
    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['newpasswd'])
        if commit:
            self.user.save()
        return self.user
        
class PlanSearchForm(forms.Form):
    patientid = forms.CharField(label=_("Patient MRN"), required=False)
    lastname = forms.CharField(label=_("Last Name"), required=False)
    firstname = forms.CharField(label=_("First Name"), required=False)
    planname = forms.CharField(label=_("Plan Name"), required=False)
    planstatus = forms.ChoiceField(label=_("Status"),
                                   choices=PLAN_STATUS_CHOICES,
                                   required=False)
    apprvstatus = forms.ChoiceField(label=_("Apprv"),
                                   choices=APPRV_STATUS_CHOICES,
                                   required=False)
    orderby = forms.ChoiceField(label=_("Order"),
                              choices=ORDER_BY_CHOICES,
                              initial='-LastModifiedDateTime')
    maxentry = forms.ChoiceField(label=_("Max plan #"),
                                choices=MAX_ENTRY_CHOICES,
                                initial='All')
    def __init__(self, *args, **kwargs):
        super(PlanSearchForm,self).__init__(*args, **kwargs)
        if not self.fields['planstatus'].choices[0][0]=='':
            self.fields['planstatus'].choices.insert(0,('',_('All')))
        if not self.fields['apprvstatus'].choices[0][0]=='':
            self.fields['apprvstatus'].choices.insert(0,('',_('All')))

class PlanStatusForm(forms.Form):
    planstatus = forms.ChoiceField(label=_("Status"),
                                   choices=PLAN_STATUS_CHOICES,
                                   initial="Active")
    username = forms.CharField(label=_("Username"))
    password = forms.CharField(label=_("Password"),widget=forms.PasswordInput)
    def __init__(self, user, *args, **kwargs):
        self.authuser = user
        super(PlanStatusForm, self).__init__(*args, **kwargs)        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            self.authuser = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(_('User Dose Not Exist!'))
        return username
    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            username = self.cleaned_data['username']
            self.authuser = User.objects.get(username=username)
        except:
            raise forms.ValidationError(_('Username and Password Not Match!'))
            
        try:
            if not self.authuser.check_password(password):
                raise forms.ValidationError(_('Incorrect Password, Try Again!'))
        except User.DoesNotExist:
            raise forms.ValidationError(_('User Dose Not Exist!'))
        return password
    
class TreatmentPlanForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TreatmentPlanForm, self).__init__(*args, **kwargs)
        active_machine = MACHINE.objects.filter(Status__exact='Active')
        active_filter = FILTER.objects.filter(Status__exact='Active'
                                              ).filter(Machine__in=active_machine)
        self.fields['Filter'].queryset = \
            NOMINALCALIBRATION.objects.filter(Status__exact='Active' #Active__exact=True
                                       ).filter(Filter__in=active_filter)
        self.fields['Cone'].queryset = \
            CONE.objects.filter(Status__exact='Active'
                                ).filter(Machine__in=active_machine)
        
    PlanName = forms.CharField(label=_("Plan Name"), widget=forms.TextInput(attrs={'size':'30'}))
    PatientId = forms.CharField(label = _("Patient MRN"), widget=forms.TextInput(attrs={'size':'30'}))
    LastName = forms.CharField(label = _("Last Name"), widget=forms.TextInput(attrs={'size':'30'}))
    FirstName = forms.CharField(label = _("First Name"), required=False, widget=forms.TextInput(attrs={'size':'30'}))
    MiddleName = forms.CharField(label = _("Middle Name"), required=False, widget=forms.TextInput(attrs={'size':'30'}))
    DOB = forms.DateField(label = _("DOB (yyyy-mm-dd)"), widget=forms.TextInput(attrs={'size':'30'}))
    
    TotalDose = forms.FloatField(label=_("Total Dose (cGy)"), widget=forms.TextInput(attrs={'size':'30'}))
    Fractions = forms.IntegerField(label=_('Fractions'),widget=forms.TextInput(attrs={'size':'30'}))
    TargetTissue = forms.ChoiceField(label=_('Target Medium'),
                                     choices=MEDIUM_CHOICES,
                                     initial='StriatedMuscle')
    PrescriptionDepth = forms.FloatField(label=_("Prescript. Depth (cm)"), initial=0, widget=forms.TextInput(attrs={'size':'30'}))

    CutoutRequired = forms.BooleanField(label=_("Cutout Required"),required=False)
    CutoutShape = forms.ChoiceField(label=_("Cutout Shape"),choices=SHAPE_CHOICES, initial='Oval')
    CutoutLength = forms.FloatField(label=_("Cutout Length (cm)"),initial=0,widget=forms.TextInput(attrs={'size':'30'}))
    CutoutWidth = forms.FloatField(label=_("Cutout Width (cm)"),initial=0,widget=forms.TextInput(attrs={'size':'30'}))
    CutoutThickness = forms.FloatField(label=_("Cutout Thickness (cm)"),initial=0.2, widget=forms.TextInput(attrs={'size':'30'}))
    StandOut = forms.FloatField(label=_("Stand In(-)/Out(+) (cm)"), widget=forms.TextInput(attrs={'size':'30'}))
    SpecifyROF = forms.BooleanField(label=_("User Specify REF"),required=False)
    ROF = forms.FloatField(label=_("Relative Exposure Factor"),initial=0,widget=forms.TextInput(attrs={'size':'30'}))
    Comment = forms.CharField(label=_('Comment'),
                              max_length=512,
                              required=False,
                              widget=forms.Textarea(
                                attrs={'cols':'50', 'rows':'3'})
                              )

    PDD = forms.FloatField(initial=100, widget=forms.HiddenInput)
    FCD = forms.FloatField(initial=0, widget=forms.HiddenInput)           # Focal Calib-Position Distance
    FSD = forms.FloatField(initial=0, widget=forms.HiddenInput)           # Focal Surface Distance
    ISF = forms.FloatField(initial=0, widget=forms.HiddenInput)           # Inverse Square Factor
    Dequiv = forms.FloatField(initial=0, widget=forms.HiddenInput)        # Equivalent Diameter
    DequivCalib = forms.FloatField(initial=0, widget=forms.HiddenInput)   # Equiv. Diameter at Cutout End
    DequivSurface = forms.FloatField(initial=0, widget=forms.HiddenInput)   # Equiv. Diameter at Medium Surface
    KR_air_CalibCone = forms.FloatField(initial=0, widget=forms.HiddenInput)  # Kerma Rate in Air for Calib. Pos.
    KR_air = forms.FloatField(initial=0, widget=forms.HiddenInput)    # Kerma Rate in Air for Pt. Surface
    BSF_wat = forms.FloatField(initial=0, widget=forms.HiddenInput)       # Back Scattering Factor for Water
    BSF_ConeEnd = forms.FloatField(initial=0, widget=forms.HiddenInput)       # Back Scattering Factor for Water
    MassAbs_WatAir_air = forms.FloatField(initial=0, widget=forms.HiddenInput)    # Mass Abs. Ratio
    DR_wat = forms.FloatField(initial=0, widget=forms.HiddenInput)    # Dose Rate at Water Surface
    C_MedWat = forms.FloatField(initial=0, widget=forms.HiddenInput)  # Medium Water convert factor Mu_med_wat
    B_MedWat = forms.FloatField(initial=0, widget=forms.HiddenInput)  # Bmed/Bwat. See Table XI and Eq. 12.
    DR_med = forms.FloatField(initial=0, widget=forms.HiddenInput)    # Dose Rate at Medium Surface
    DosePerFrac = forms.FloatField(initial=0, widget=forms.HiddenInput)   # Dose Per Fraction
    TxTime = forms.FloatField(initial=0, widget=forms.HiddenInput)    # Treatment Time
    SXTCalcVersion = forms.CharField(widget=forms.HiddenInput)
    DoseCalibDate = forms.DateField(widget=forms.HiddenInput)
    ModifiedByUser = forms.CharField(widget=forms.HiddenInput)
    
    PlanStatus = forms.CharField(initial='Active',required=False,widget=forms.HiddenInput)
    StatusChangedBy = forms.CharField(initial='nobody',required=False,widget=forms.HiddenInput)
    ApprvStatus = forms.CharField(initial='NotApproved',required=False,widget=forms.HiddenInput)
    ApprovedBy = forms.CharField(initial='nobody',required=False,widget=forms.HiddenInput)
    #ApprvDateTime = forms.DateTimeField(initial=datetime.datetime.now,required=False)
    #StatusChangeDateTime = forms.DateTimeField(initial=datetime.datetime.now,required=False)

    class Meta:
        model = TREATMENTPLAN
        fields = "__all__"
        #exclude=('PlanStatus','StatusChangeDateTime','StatusChangedBy',
        #         'ApprvStatus','ApprovedBy','ApprvDateTime',)
    
    def clean_PrescriptionDepth(self):
        PrescriptionDepth  = self.cleaned_data['PrescriptionDepth']
        if PrescriptionDepth != 0:
            raise forms.ValidationError(_('Non-ZERO depth NOT supported yet!'))
        return PrescriptionDepth

    def clean_Fractions(self):
        Fractions = self.cleaned_data['Fractions']
        if Fractions <= 0:
            raise forms.ValidationError(_('Fractions must be Positive Integer!'))
        return Fractions

    def clean_DOB(self):
        DOB = self.cleaned_data['DOB']
        if DOB > datetime.date.today():
            raise forms.ValidationError(_('DOB cannot be in the future!'))
        if DOB < datetime.date.today()-datetime.timedelta(days=365*150):
            raise forms.ValidationError(_('More than 150 years old?'))
        return DOB
    
    def clean(self):
        cleaned_data = super(TreatmentPlanForm, self).clean()
        
        Filter = self.cleaned_data.get('Filter',None)
        Cone = self.cleaned_data.get('Cone',None)
        
        FilterConeOK = True
        if not Filter:
            errmsg = _('This field is required')
            self._errors['Filter'] = self.error_class([errmsg])
            FilterConeOK = False
        elif Filter.Filter.Machine.Status!='Active':
            errmsg = _('This X-ray Machine is Not Aactive!')
            self._errors['Filter'] = self.error_class([errmsg])
            FilterConeOK = False                         
        if not Cone:
            errmsg = _('This field is required.')
            self._errors['Cone'] = self.error_class([errmsg])
            FilterConeOK = False
        elif Cone.Machine.Status!='Active':
            errmsg = _('This X-Ray Machines is Not Active!')
            self._errors['Cone'] = self.error_class([errmsg])
            FilterConeOK = False
        if not FilterConeOK:
            return cleaned_data
        
        if Filter.Filter.Machine.pk != Cone.Machine.pk:
            errmsg = _('Filter and Cone are NOT for the same X-Ray Machine!')
            self._errors['Filter'] = self.error_class([errmsg])
            self._errors['Cone']   = self.error_class([errmsg])
            return cleaned_data
        
        CutoutRequired = self.cleaned_data['CutoutRequired']
        if CutoutRequired:
            CutoutShape = self.cleaned_data['CutoutShape']
            CutoutLength = self.cleaned_data['CutoutLength']
            CutoutWidth = self.cleaned_data['CutoutWidth']
            CutoutThickness = self.cleaned_data['CutoutThickness']
            CutoutOK = True
            
            if CutoutLength<=0:
                errmsg_length = _('Must be greater than Zero!')
                self._errors['CutoutLength'] = self.error_class([errmsg_length])
                CutoutOK = False
            elif CutoutLength>=Cone.getMaxDimension(): #Cone.Diameter:
                errmsg_length = _('Must be less than cone size!')
                self._errors['CutoutLength'] = self.error_class([errmsg_length])
                CutoutOK = False
                
            if CutoutWidth<=0:
                errmsg_width = _('Must be greater than Zero!')
                self._errors['CutoutWidth'] = self.error_class([errmsg_width])
                CutoutOK = False
            elif CutoutWidth>=Cone.getMaxDimension(): #Cone.Diameter:
                errmsg_width = _('Must be less than cone size!')
                self._errors['CutoutWidth'] = self.error_class([errmsg_width])
                CutoutOK = False
                
            if CutoutOK and CutoutShape=='Rectangle':
                #if CutoutLength**2+CutoutWidth**2 >= Cone.Diameter**2:
                if math.sqrt(CutoutLength**2+CutoutWidth**2) >= Cone.getMaxDimension():
                    errmsg_length = _('Diagonal length must be less than cone size!')
                    errmsg_width  = _('Diagonal length must be less than cone size!')
                    self._errors['CutoutLength'] = self.error_class([errmsg_length])
                    self._errors['CutoutWidth']  = self.error_class([errmsg_width])
                    CutoutOK = False
                    
            if CutoutThickness<0.1:
                errmsg_thickness = _('Must be no less than 0.1 cm!')
                self._errors['CutoutThickness'] = self.error_class([errmsg_thickness])
                CutoutOK = False
            elif CutoutThickness>=1.0:
                errmsg_thickness = _('Must be less than 1.0 cm!')
                self._errors['CutoutThickness'] = self.error_class([errmsg_thickness])
                CutoutOK = False
            if not CutoutOK:        
                del cleaned_data['CutoutLength']
                del cleaned_data['CutoutWidth']
                del cleaned_data['CutoutThickness']
        return cleaned_data
            
class DoctorForm(forms.ModelForm):
    class Meta:
        model = DOCTOR
        fields = "__all__"

