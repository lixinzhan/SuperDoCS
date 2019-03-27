from django.utils.translation import ugettext_lazy as _

ErrorCode = {
    # For General Unknown Errors
    'E0000': _('Unknown Error. '),
    
    # django models
    'E0010': _('Unknown Error in Models'),
    
    # django tables
    'E0020': _('Unknown Error in Tables'),
    
    # django views
    'E0030': _('Unknown Error in views'),
    'E0031': _('Filter/Applicator set not calib\'d OR calib\'d more than once. '),
    'E0032': _('None or more than one matching Active CALIBRATION found!'),
    'E0033': _('No ROF found for the Filter/Applicator set!'),
    
    # --- for TG61 Data Processing --- #
    
    # BSF_Wat
    'E0100': _('BSF_Wat: SSD Out of Range. '),
    'E0101': _('BSF_Wat: DFLD Out of Range. '),
    'E0102': _('BSF_Wat: HVL Out of Range. '),
    'E0103': _('BSF_Wat: Wrong HVL Unit!'),
    'E0104': _('BSF_Wat: Value Error!'),
    
    'E0110': _('CMedWat: Can Not Find HVL Material. '),
    'E0111': _('CMedWat: HVL Out of Range. '),
    'E0112': _('CMedWat: Unknown Error. '),
    
    # BSF_BoneWat
    'E0120': _('BSF_BoneWat: Incorrect HVL Unit. '),
    'E0121': _('BSF_BoneWat: HVL Out of Range. '),
    'E0122': _('BSF_BoneWat: FLD Out of Range. '),
    'E0123': _('BSF_BoneWat: SSD Out of Range. '),
    'E0124': _('BSF_BoneWat: Unknown Error. '),
    
    # BSF_CloseCone
    'E0130': _('BSF_CloseCone: Incorrect Cone End'),

    # for Curve Fitting
    'E1000': _('Unknown cutout curve fitting method. '),
    'E1001': _('Cutout equiv. diameter too small for the cone. '),
    'E1002': _('Cutout equiv. diameter too big for the cone. '),
    'E1003': _('Cutout thickness dose not match calibration. '),
    'E1004': _('Curve Fitting Unknown Error'),
    
}
