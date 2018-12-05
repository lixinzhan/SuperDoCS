import math
import datetime
import numpy as np

from django.conf import settings
from .models import *
from .forms import *
from protocols.TG61.CMedWat import CMedWat
from protocols.TG61.BSF_Wat import BSF_Wat
from protocols.TG61.BSF_CloseCone import BSF_CloseCone
from protocols.TG61.BSF_BoneWat import BSF_BoneWat
from protocols.TG61.Mu_WatAir_air import Mu_WatAir_air
from .curve_fitting import getROF
from common.errcode import ErrorCode

def copyPlanSetup(plan,oldplan):
    plan.PlanName          = oldplan.PlanName + '_copy'
    plan.PatientId         = oldplan.PatientId
    plan.LastName          = oldplan.LastName
    plan.FirstName         = oldplan.FirstName
    plan.MiddleName        = oldplan.MiddleName
    plan.DOB               = oldplan.DOB
    #plan.TotalDose         = oldplan.TotalDose
    #plan.Fractions         = oldplan.Fractions
    plan.PrescriptionDepth = oldplan.PrescriptionDepth
    plan.TargetTissue      = oldplan.TargetTissue
    plan.Filter            = oldplan.Filter
    plan.Cone              = oldplan.Cone
    plan.CutoutRequired    = oldplan.CutoutRequired
    plan.CutoutLength      = oldplan.CutoutLength
    plan.CutoutShape       = oldplan.CutoutShape
    plan.CutoutWidth       = oldplan.CutoutWidth
    plan.CutoutThickness   = oldplan.CutoutThickness
    plan.StandOut          = oldplan.StandOut
    plan.SpecifyROF        = oldplan.SpecifyROF
    plan.ROF               = oldplan.ROF
    
    return True


def getPlanFormData(plan,planform):
    if planform.is_valid():
        plan.PlanName = planform.cleaned_data['PlanName']
        plan.PatientId = planform.cleaned_data['PatientId']
        plan.LastName = planform.cleaned_data['LastName']
        plan.FirstName = planform.cleaned_data['FirstName']
        plan.MiddleName = planform.cleaned_data['MiddleName']
        plan.DOB = planform.cleaned_data['DOB']
        plan.TotalDose = planform.cleaned_data['TotalDose']
        plan.DosePerFrac = planform.cleaned_data['DosePerFrac']
        plan.Fractions = planform.cleaned_data['Fractions']
        plan.PrescriptionDepth = planform.cleaned_data['PrescriptionDepth']
        plan.TargetTissue = planform.cleaned_data['TargetTissue']
        plan.Filter = planform.cleaned_data['Filter'] # plan.Filter is Calibratin
        plan.Cone = planform.cleaned_data['Cone']
        plan.CutoutRequired = planform.cleaned_data['CutoutRequired']
        plan.CutoutLength = planform.cleaned_data['CutoutLength']
        plan.CutoutShape = planform.cleaned_data['CutoutShape']
        plan.CutoutWidth = planform.cleaned_data['CutoutWidth']
        plan.CutoutThickness = planform.cleaned_data['CutoutThickness']
        plan.StandOut = planform.cleaned_data['StandOut']
        plan.PDD = planform.cleaned_data['PDD']
        plan.DosePerFrac = planform.cleaned_data['DosePerFrac']
        plan.FCD = planform.cleaned_data['FCD']
        plan.FSD = planform.cleaned_data['FSD']
        plan.ISF = planform.cleaned_data['ISF']
        plan.SpecifyROF = planform.cleaned_data['SpecifyROF']
        plan.ROF = planform.cleaned_data['ROF']
        plan.Dequiv = planform.cleaned_data['Dequiv']
        plan.DequivCalib = planform.cleaned_data['DequivCalib']
        plan.DequivSurface = planform.cleaned_data['DequivSurface']
        plan.KR_air = planform.cleaned_data['KR_air']
        plan.KR_air_CalibCone = planform.cleaned_data['KR_air_CalibCone']
        plan.BSF_wat = planform.cleaned_data['BSF_wat']
        plan.BSF_ConeEnd = planform.cleaned_data['BSF_ConeEnd']
        plan.MassAbs_WatAir_air = planform.cleaned_data['MassAbs_WatAir_air']
        plan.DR_wat = planform.cleaned_data['DR_wat']
        plan.C_MedWat = planform.cleaned_data['C_MedWat']
        plan.B_MedWat = planform.cleaned_data['B_MedWat']
        plan.DR_med = planform.cleaned_data['DR_med']
        plan.TxTime = planform.cleaned_data['TxTime']
        plan.ModifiedByUser = planform.cleaned_data['ModifiedByUser']
        plan.SXTCalcVersion = planform.cleaned_data['SXTCalcVersion']
        plan.DoseCalibDate = planform.cleaned_data['DoseCalibDate']
        plan.ApprovedBy = planform.cleaned_data['ApprovedBy']
        #plan.ApprvDateTime = planform.cleaned_data['ApprvDateTime']
        plan.ApprvStatus = planform.cleaned_data['ApprvStatus']
        plan.PlanStatus = planform.cleaned_data['PlanStatus']
        #plan.StatusChangeDateTime = planform.cleaned_data['StatusChangeDateTime']
        plan.StatusChangedBy = planform.cleaned_data['StatusChangedBy']
    else:
        return False
    
    return True

def calcTxPlan(plan, errlist):
    conecalib = plan.Filter.Cone # The Calibration Cone. plan.Filter <--> Calibration
    dr = CALIBRATION.objects.get(id=plan.Filter.id)
    
    # Just use the P_stem_air for calibration (1.0 actually)
    # Field change may result in the change of P_stem_air,
    # but we assume no change for cylindrical ion chamber.
    P_stem_air = plan.Filter.P_stem
            
    if plan.CutoutRequired:
        if plan.CutoutShape=='Oval':
            plan.Dequiv = 2.0 * plan.CutoutLength * plan.CutoutWidth \
                          /(plan.CutoutLength + plan.CutoutWidth)
        elif plan.CutoutShape=='Rectangle':
            plan.Dequiv = 4.0*plan.CutoutLength * plan.CutoutWidth \
                          /(math.sqrt(math.pi)*(plan.CutoutLength + plan.CutoutWidth))
    else:
        plan.Dequiv = plan.Cone.getEquivDiameter() #plan.Cone.Diameter
        plan.CutoutThickness = 0
        
    plan.FCD = conecalib.FSD # Focal Calib. Cone-End Distance
    
    # True for ConeEndStandIn: StandIn is from Cone End, but StandOut is from Cutout End.
    # False for ConeEndStandIn: Both StandIn and StandOut are from Cutout End.
    ConeEndStandIn = False
    if plan.StandOut<0 and ConeEndStandIn:                    
        plan.FSD = plan.Cone.FSD + plan.StandOut # GRRCC convention.
    else:
        plan.FSD = plan.Cone.FSD + plan.CutoutThickness + plan.StandOut
    # plan.ISF = (plan.FCD/plan.FSD)**2
    
    FocalCutoutDist = plan.Cone.FSD + plan.CutoutThickness # Focal Spot to Cutout End
    plan.DequivCalib = plan.Dequiv * plan.FCD/FocalCutoutDist # get Dequiv @ calib cone postion.
    plan.DequivSurface = plan.Dequiv * plan.FSD/FocalCutoutDist      # get Dequiv @ medium surface.
    
    # Derivation:
    #         K_air(cal) * REF_cone ==> K_air(cone-end)
    #         K_air(cone-end) * (FSD_cone/FSD_cutout)**2 ==> K_air(cutout-end-position) at the position but without cutout yet
    #         K_air(cutout-end) * REF_cutout ==> K_air(cutout-end)  with cutout now
    #         K_air(cutout-end) * (FSD_cutout/FSD_media-surface) **2 ==> K_air(media surface)
    # Hence, K_air(cal) * ISF * REF ==> K_air(media surface)
    # with       ISF = (FSD_cone/FSD_cutout)**2 * (FSD_cutout/FSD_media-surface)**2
    #                = (FSD_cone/FSD_media-surface)**2
    # and        REF = REF_cone * REF_cutout
    
    plan.ISF = (plan.Cone.FSD/plan.FSD)**2  # NOT (FocalCutoutDist/plan.FSD)**2
    
    # Air Kerma rate at calib cone end
    plan.KR_air_CalibCone = dr.DR_Air
    
    if not plan.SpecifyROF:
        try:   # plan.Filter is actually the calibration of a filter here.
            ROFEntry = OUTPUTFACTOR.objects.get(Filter=plan.Filter.id, Cone=plan.Cone.id)
            #if plan.CutoutRequired:
            try:
                plan.ROF=getROF(ROFEntry,plan.Dequiv, plan.CutoutRequired, plan.CutoutThickness)
            except ValueError as err:
                plan.ROF = 0
                errlist.append(err[0]) #'Cutout Out of Commissioned Range. '
            except LookupError as err:
                plan.ROF = 0
                errlist.append(err[0]) #'Unknown Cutout REF Fitting Method. '
            except:
                plan.ROF = 0
                errlist.append('E1004') #'Unknown Error in CurveFitting. '
            #else:
            #    plan.ROF = ROFEntry.ConeFactor
        except:
            plan.ROF = 0
            errlist.append('E0031') #'Filter/Cone Combination Not Commissioned. '
        autoROF = plan.ROF
    #else:
    #    customROF = 
        
    # Air Kerma rate at target surface
    # plan.KR_air = plan.KR_air_CalibCone * plan.Filter.P_stem * plan.ISF * plan.ROF
    plan.KR_air = plan.KR_air_CalibCone * plan.Filter.P_stem * plan.ISF * plan.ROF
            
    # get backscattering factor and mass absorption coefficient
    # Note plan.Filter is actually pointing to class Calibration.
    # So if real Filter info is required, plan.Filter.Filter should be used.
    try: 
        bsf = BSF_Wat()
        plan.BSF_wat = bsf.getValue(plan.FSD, plan.DequivSurface,
                                plan.Filter.Filter.HVL,
                                plan.Filter.Filter.HVLUnit)
    except ValueError as err:
        plan.BSF_wat = 0.0
        errlist.append(err[0]) #'Bw: FLD/HVL/FSD Out of Range. '
    if plan.Cone.ConeEnd=="Open":
        plan.BSF_ConeEnd = 1.0
    elif plan.Cone.ConeEnd=="PMMA3p2":
        bsfcc = BSF_CloseCone()
        plan.BSF_ConeEnd = bsfcc.getValue(plan.DequivSurface,
                                          plan.Filter.Filter.HVL,
                                          plan.Filter.Filter.HVLUnit)
    else:
        plan.BSF_ConeEnd = 0.0
        errlist.append('E0130')
    
    mu = Mu_WatAir_air()
    plan.MassAbs_WatAir_air = mu.getValue(plan.Filter.Filter.HVLUnit,
                                          plan.Filter.Filter.HVL)
    
    # Dose rate at target surface is medium is water        
    plan.DR_wat = plan.KR_air * plan.BSF_wat * plan.BSF_ConeEnd * \
                  plan.MassAbs_WatAir_air
            
    # C_MedWat
    medium = plan.TargetTissue
    if medium=='Air':
        plan.C_MedWat = 0.0 #np.nan
        plan.B_MedWat = 0.0 #np.nan
        plan.DR_med = plan.KR_air
    elif medium=='Water':
        plan.C_MedWat = 1.0
        plan.B_MedWat = 1.0
        plan.DR_med = plan.DR_wat
    else:
        try:
            cmw = CMedWat()
            plan.C_MedWat = cmw.getValue(plan.Filter.Filter.HVL,
                                     plan.Filter.Filter.HVLUnit, medium)
        except LookupError as err:
            plan.C_MedWat = 0
            errlist.append(err[0]) #'CMedWat: Incorrect HVL Unit or Incorrect Material. '
        except ValueError as err:
            plan.C_MedWat = 0
            errlist.append(err[0]) #'CMedWat: HVL Out of Range. '
            
        if medium=='CompactBone':
            try:
                bmw = BSF_BoneWat()
                plan.B_MedWat = bmw.getValue(plan.FSD, plan.DequivSurface,
                                         plan.Filter.Filter.HVL,
                                         plan.Filter.Filter.HVLUnit)
            except ValueError as err:
                plan.B_MedWat = 0
                errlist.append(err[0]) #'BSF_BoneWat: FLD/SSD/HVL Out of Table Range. '
            except:
                plan.B_MedWat = 0
                errlist.append('E0124') #'BSF_BoneWat: Unknow Error. '
        else:
            plan.B_MedWat = 1.0
        plan.DR_med = plan.DR_wat * plan.C_MedWat * plan.B_MedWat
            
    plan.DosePerFrac = plan.TotalDose / plan.Fractions
            
    plan.TxTime = plan.DosePerFrac/plan.DR_med + plan.Filter.Filter.EndEffect
    plan.CalculateDateTime = datetime.datetime.now
    plan.SXTCalcVersion = settings.VERSION
    plan.DoseCalibDate = datetime.datetime.date(plan.Filter.MeasurementDateTime)

    return plan.TxTime
