import numpy as np

def CustomizedCutoutROF(ROFTable, Dequiv):
    ''' ROFTable: Table in DB contains ConeFactor and 
            CutoutROF fitting parameters: A, B, C, D, E, F, G.

        Dequiv: Equivalent Diameter (Cutout End if HasCutout)

        Users can implement the fitting equation here.
        Otherwise, the cutout factor is default to 1.0 for all cutouts,
        which should result in the change of final results < 1.0% in most cases.
    '''

    CutoutROF=1.0
    
    return CutoutROF
