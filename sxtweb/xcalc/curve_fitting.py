import numpy as np
from .UserCodes.rof_customize import CustomizedCutoutROF

def getCutoutFactor(ROFTable, Dequiv):
    if ROFTable.FitMethod == 'Default':
        P = ROFTable.P
        S = ROFTable.S
        U = ROFTable.U
        L = ROFTable.L
        N = ROFTable.N
        x = Dequiv
        CutoutROF = P * x**N / (L**N+x**N) + S * (1.0-np.exp(-U*x))
    elif ROFTable.FitMethod == 'Exponential':
        P = ROFTable.P
        S = ROFTable.S
        U = ROFTable.U
        x = Dequiv
        CutoutROF = P + S * (1.0-np.exp(-U*x))
    elif ROFTable.FitMethod == 'Polynomial2':
        P = ROFTable.P
        S = ROFTable.S
        U = ROFTable.U
        x = Dequiv
        CutoutROF = P + S*x + U*x**2 
    elif ROFTable.FitMethod == 'Polynomial3':
        P = ROFTable.P
        S = ROFTable.S
        U = ROFTable.U
        L = ROFTable.L
        x = Dequiv
        CutoutROF = P + S*x + U*x**2 + L*x**3
    elif ROFTable.FitMethod == 'Linear':
        P = ROFTable.P
        S = ROFTable.S
        x = Dequiv
        CutoutROF = P + S*x
    elif ROFTable.FitMethod == 'Customized':
        CutoutROF = CustomizedCutoutROF(ROFTable, Dequiv)
    else:
        raise LookupError('E1000') # unknown fitting method
        
    return CutoutROF
    

def getROF(ROFTable, Dequiv, HasCutout=False, CutoutThickness=0):
    ''' ROFTable: Table in DB contains ConeFactor and ROF fitting parameters
        Dequiv: Equivalent Diameter (Cutout End if HasCutout)
    '''

    # make sure DequivCalib is in the commissioned cutout range.
    # here, DequivMax and DequivMin are the cutout equiv. diameter range    # at the calibration position.
    if HasCutout and Dequiv < ROFTable.DequivMin:
        raise ValueError('E1001') # cutout too small
    if HasCutout and Dequiv > ROFTable.DequivMax:
        raise ValueError('E1002') # cutout too big
    if HasCutout and CutoutThickness != ROFTable.CutoutThickness:
        raise ValueError('E1003') # incorrect cutout thickness
            
    if not HasCutout:
        return ROFTable.ConeFactor

    return ROFTable.ConeFactor * getCutoutFactor(ROFTable, Dequiv)

