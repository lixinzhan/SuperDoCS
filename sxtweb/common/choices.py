from django.utils.translation import ugettext_lazy as _

# CHOICES FOR UNITS
OUTPUT_CONTROL_CHOICES = (
    ('min',_('Minutes')),
    ('MU',_('Monitor Units')),
)
HVL_UNIT_CHOICES = (
    ('mm Al', _('mm Al')),
    ('mm Cu', _('mm Cu')),
)
MEDIUM_CHOICES = (
    ('StriatedMuscle', _('ICRU striated muscle')),
    ('Skin', _('ICRP skin')),
    ('SoftTissue', _('ICRU 4-element soft tissue')),
    ('Lung', _('ICRP lung')),
    ('CompactBone', _('ICRU compact bone')),
    ('Water', _('Water')),
    ('Air', _('Air')),
)
SHAPE_CHOICES = (
    ('Oval', _('Oval/Circle')),
    ('Rectangle', _('Rectangle/Square')),
    # ('UserSpecified', _('UserSpecified')),
)
CALIB_INST_CHOICES = (
    ('NRC', _('NRC')),
)
CALIBRATION_METHOD_CHOICES = (
    ('in-Air', _('TG61 in-Air method')),
#    ('in-Phantom', 'TG61 in-Phantom method'),
)
ORDER_BY_CHOICES = (
    ('-LastModifiedDateTime', _('Change Time')),
    ('PatientId', _('Patient MRN')),
    ('LastName', _('Last Name')),
    ('FirstName', _('First Name')),
    ('PlanName', _('Plan Name')),
)
MAX_ENTRY_CHOICES = (
    ('All', _('All')),
    ('10', '10'),
    ('20', '20'),
    ('50', '50'),
    ('100','100'),
)
STATUS_CHOICES = (
    ('Active', _('Active')),
    ('Disabled', _('Disabled')),
)
HW_STATUS_CHOICES = (
    ('Active', _('Active')),
    ('Inactive', _('Inactive')),
    ('Decommissioned', _('Decommissioned')),
    ('Retired', _('Retired')),
)
PLAN_STATUS_CHOICES = (
    ('All', _('All')),
    ('Active', _('Active')),
    ('Completed', _('Completed')),  # treatment completed
    ('Retired', _('Retired')),      # partial treatment and then new plan used.
    ('Cancelled', _('Cancelled')),  # planned but never used.
)
APPRV_STATUS_CHOICES = (
    ('All', _('All')),
    ('NotApproved', _('Not Apprv\'d')),
    ('Approved',_('Approved')),
    ('UnApproved',_('UnApproved')),   # unset previous physics approval status.
)
CURVE_FITTING_CHOICES = (
    ('Default', _('Hill-Exponential')),
    ('Exponential', _('Exponential')),
    ('Hill', _('Hill')),
    ('Polynomial2', _('Polynomial2')),
    ('Polynomial3', _('Polynomial3')),
    ('Linear', _('Linear')),
    ('Customized',  _('Customized')),
)
CONE_END_CHOICES = (
    ('Open', _('Open')),
    ('PMMA3p2', _('PMMA 3.2 mm')),
)
CONE_SHAPE_CHOICES = (
    ('Circle',_('Circle')),
    ('Square',_('Square')),
    ('Rectangle',_('Rectangle')),
)
#PLAN_ACTION_CHOICES = (
#    ('CopyPlan',_('Copy Plan')),
#)
