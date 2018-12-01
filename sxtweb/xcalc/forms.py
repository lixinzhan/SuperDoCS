from django import forms
from django.utils.translation import ugettext_lazy as _

from common.choices import *
    
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
