import numpy as np
#from mpl_toolkits.mplot3d import axes3d
#import matplotlib.pyplot as plt
import scipy.interpolate as intp
from io import StringIO

class HVLAlCu:
    def __init__(self):
        '''Initialize the HVLTable by reading in data from the file specified.'''
        
        # Mass Attn Coeff for Aluminum from NIST
        self.AlMassAttenuationCoeff = np.array([
            [    1.0000,     1185.00000 ],
            [    1.5000,      402.20000 ],
            [    1.5596,      362.10000 ],
            [    1.5596,     3957.00000 ],
            [    2.0000,     2263.00000 ],
            [    3.0000,      788.00000 ],
            [    4.0000,      360.50000 ],
            [    5.0000,      193.40000 ],
            [    6.0000,      115.30000 ],
            [    8.0000,       50.33000 ],
            [   10.0000,       26.23000 ],
            [   15.0000,        7.95500 ],
            [   20.0000,        3.44100 ],
            [   30.0000,        1.12800 ],
            [   40.0000,        0.56850 ],
            [   50.0000,        0.36810 ],
            [   60.0000,        0.27780 ],
            [   80.0000,        0.20180 ],
            [  100.0000,        0.17040 ],
            [  150.0000,        0.13780 ],
            [  200.0000,        0.12230 ],
            [  300.0000,        0.10420 ],
            [  400.0000,        0.09276 ],
            [  500.0000,        0.08445 ],
            [  600.0000,        0.07802 ],
            [  800.0000,        0.06841 ],
            [ 1000.0000,        0.06146 ],
            [ 1250.0000,        0.05496 ],
            [ 1500.0000,        0.05006 ],
            [ 2000.0000,        0.04324 ],
            [ 3000.0000,        0.03541 ],
            [ 4000.0000,        0.03106 ],
            [ 5000.0000,        0.02836 ],
            [ 6000.0000,        0.02655 ],
            [ 8000.0000,        0.02437 ],
            [10000.0000,        0.02318 ],
            [15000.0000,        0.02195 ],
            [20000.0000,        0.02168 ] ], dtype=np.float)
        
        # Mass Attn Coeff for Copper from NIST
        self.CuMassAttenuationCoeff = np.array([
            [    1.00000,    10570.00000 ],
            [    1.04695,     9307.00000 ],
            [    1.09610,     8242.00000 ],
            [    1.09610,     9347.00000 ],
            [    1.50000,     4418.00000 ],
            [    2.00000,     2154.00000 ],
            [    3.00000,      748.80000 ],
            [    4.00000,      347.30000 ],
            [    5.00000,      189.90000 ],
            [    6.00000,      115.60000 ],
            [    8.00000,       52.55000 ],
            [    8.97890,       38.29000 ],
            [    8.97890,      278.40000 ],
            [   10.00000,      215.90000 ],
            [   15.00000,       74.05000 ],
            [   20.00000,       33.79000 ],
            [   30.00000,       10.92000 ],
            [   40.00000,        4.86200 ],
            [   50.00000,        2.61300 ],
            [   60.00000,        1.59300 ],
            [   80.00000,        0.76300 ],
            [  100.00000,        0.45840 ],
            [  150.00000,        0.22170 ],
            [  200.00000,        0.15590 ],
            [  300.00000,        0.11190 ],
            [  400.00000,        0.09413 ],
            [  500.00000,        0.08362 ],
            [  600.00000,        0.07625 ],
            [  800.00000,        0.06605 ],
            [ 1000.00000,        0.05901 ],
            [ 1250.00000,        0.05261 ],
            [ 1500.00000,        0.04803 ],
            [ 2000.00000,        0.04205 ],
            [ 3000.00000,        0.03599 ],
            [ 4000.00000,        0.03318 ],
            [ 5000.00000,        0.03177 ],
            [ 6000.00000,        0.03108 ],
            [ 8000.00000,        0.03074 ],
            [10000.00000,        0.03103 ],
            [15000.00000,        0.03247 ],
            [20000.00000,        0.03408 ] ], dtype=np.float)
                
        self.AlDensity = np.float(2.699) # g/cm3
        self.CuDensity = np.float(8.960) # g/cm3
        self.AlCharactE = np.float(1.5596) # keV
        self.CuCharactE = np.float(8.97890) # keV

        self.AlHVLTable = np.array(self.AlMassAttenuationCoeff)
        self.AlHVLTable[:,1]=np.log(2.0)*10.0/(self.AlMassAttenuationCoeff[:,1]*self.AlDensity)
        self.CuHVLTable = np.array(self.CuMassAttenuationCoeff)
        self.CuHVLTable[:,1]=np.log(2.0)*10.0/(self.CuMassAttenuationCoeff[:,1]*self.CuDensity)
                
        # find the index for charactoristic position.
        self.AlCharactIndex = []
        for i in range(len(self.AlMassAttenuationCoeff)):
            if (self.AlMassAttenuationCoeff[i][0]-self.AlCharactE)<1.0e-6:
                self.AlCharactIndex.append(i)
        self.CuCharactIndex = []
        for i in range(len(self.CuMassAttenuationCoeff)):
            if (self.CuMassAttenuationCoeff[i][0]-self.CuCharactE)<1.0e-6:
                self.CuCharactIndex.append(i)
                
            
    def showTables(self):
        '''Show the contents of the table. It is often for debugging'''
        print('Al HVL Table')
        print((self.AlHVLTable))
        print('Cu HVL Table')
        print((self.CuHVLTable))

    def getHVL(self, Eeff, HVLUnit = 'mm Al', IntpSpace='Logrithm'):
        '''Obtain HVL value from Effective Energy
        '''
        if HVLUnit == 'mm Al':
            HVLTable = self.AlHVLTable
            ich = self.AlCharactIndex
            ech = self.AlCharactE
        elif HVLUnit == 'mm Cu':
            HVLTable = self.CuHVLTable
            ich = self.CuCharactIndex
            ech = self.CuCharactE
        else:
            print('Unknown HVL Material. Check please.')

        if Eeff>=ech and Eeff<=HVLTable[-1,0]:
            ## Perform cubic spline interpolation
            uindx = ich[-1]
            if IntpSpace=='Logrithm': # in the logrithm space
                tck = intp.splrep(np.log(HVLTable[uindx:,0]),HVLTable[uindx:,1],s=0)
                result = intp.splev(np.log(Eeff),tck,der=0)
            else: # in the original linear space
                tck = intp.splrep(HVLTable[uindx:,0],HVLTable[uindx:,1],s=0)
                result = intp.splev(Eeff,tck,der=0)
        elif Eeff<ech and Eeff>=HVLTable[0,0]:
            ## Perform linear interpolation
            lindx = ich[0]
            f = intp.interp1d(HVLTable[lindx:,0],HVLTable[lindx:,1])
            result = f(Eeff)
        else:
            result = np.nan
            
        return result

    def getEffectiveEnergy(self, HVL, HVLUnit = 'mm Al', IntrpMethod='Linear'):
        '''Obtain HVL value from Effective Energy
        '''
        if HVLUnit == 'mm Al':
            HVLTable = self.AlHVLTable
            ich = self.AlCharactIndex[-1]
            hvlch = self.AlHVLTable[ich,1]
            imax = len(self.AlHVLTable)
            hvlmax = np.max(self.AlHVLTable)
        elif HVLUnit == 'mm Cu':
            HVLTable = self.CuHVLTable
            ich = self.CuCharactIndex[-1]
            hvlch = self.CuHVLTable[ich,1]
            hvlmax = np.max(self.CuHVLTable[:,1])
            imax = 38 # the index for hvlmax. It should be in a more elegent way.
        else:
            print('Unknown HVL Material. Check please.')

        # only perform interpolation for the monochronic part.
        # the part below the charactoristic energy is not considered.
        # the part after the hvlmax is not considered either.
        if HVL>=hvlch and HVL<=hvlmax: #HVL<=HVLTable[-1,0]:
            ## Perform cubic spline interpolation
            if IntrpMethod=='Linear':
                f = intp.interp1d(HVLTable[ich:imax,1],HVLTable[ich:imax,0])
                result = f(HVL)
            elif IntrpMethod == 'CubicSplineLog':
                tck = intp.splrep(HVLTable[ich:imax,1],np.log(HVLTable[ich:imax,0]),s=0)
                result = np.exp(intp.splev(HVL,tck,der=0))
            else: # CubicSpline Regular
                tck = intp.splrep(HVLTable[ich:imax,1],HVLTable[ich:imax,0],s=0)
                result = intp.splev(HVL,tck,der=0)
        else:
            result = np.nan
            
        return result
        
    def convertHVLUnit(self, HVL_in, HVLUnit_in):
        if HVLUnit_in == 'mm Al':
            HVLUnit_out = 'mm Cu'
        elif HVLUnit_in == 'mm Cu':
            HVLUnit_out = 'mm Al'
        
        Energy = self.getEffectiveEnergy(HVL_in, HVLUnit_in)
        HVL_out = self.getHVL(Energy, HVLUnit_out)
        
        return (HVL_out, HVLUnit_out)


#hvl = HVLAlCu()
#print hvl.convertHVLUnit(5, 'mm Cu')
#Table = HVLTable()
#Table.showTables()
##x = np.linspace(np.log(1.0),np.log(20000.0),100)
##x = np.exp(x)
##
##y=[]
##y1=[]
##for xx in x:
##    y.append(Table.getHVL(xx,'Cu'))
##    y1.append(Table.getHVL(xx,'Cu',IntpSpace='Linear'))
##
##plt.figure(1)
##x=np.log(x); y=np.log(y); y1=np.log(y1)
##plt.plot(x,y,'r-',x,y1,'x',np.log(Table.CuHVLTable[:,0]),np.log(Table.CuHVLTable[:,1]),'o')
###plt.plot(x,y,'r-',x,y1,'x',Table.CuHVLTable[:,0],Table.CuHVLTable[:,1],'o')
##plt.xlabel('$E_{eff}$')
##plt.ylabel('HVL')
###plt.xlim(np.log(1.0),np.log(2.0))
###plt.xlim(1.0,15.0)
###plt.ylim(0.0,0.0001)
##plt.show()
#
#
## x = np.linspace(0.0071,118.0,100) # for Al
#x = np.linspace(0.002779,25.1659,100) # for Cu
#y=[]
#for xx in x:
#    y.append(Table.getEffectiveEnergy(xx,'Cu'))#,IntrpMethod='CubicSpline'))
#
#plt.figure(1)
#plt.plot(y,x,'r-',Table.CuHVLTable[:,0],Table.CuHVLTable[:,1],'o')
##plt.plot(x,y,'r-x',Table.AlHVLTable[:,1],Table.AlHVLTable[:,0],'o')
##x=np.log(x)
##plt.plot(x,np.log(y),'r-x',np.log(Table.AlHVLTable[:,1]),np.log(Table.AlHVLTable[:,0]),'o')
##plt.plot(x,np.log(y),'r-x',np.log(Table.CuHVLTable[:,1]),np.log(Table.CuHVLTable[:,0]),'-o')
#plt.show()
#
