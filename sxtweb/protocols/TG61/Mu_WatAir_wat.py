import numpy as np
import scipy.interpolate as intp
import os

class MuWatAirTable:
    def __init__(self):
        '''Initialize the MuWatAirTable by reading in data from the file specified.
            The first read in row should contains the column definition.
        '''
        FileName = os.path.abspath(os.path.join(os.getcwd(),
                                                'Data/Mu_WatAir_wat.dat'))        
        fh = open(FileName)
        LineElements = []
        MWATable = []
        for line in fh:
            line = line.strip()
            if len(line)>0 and line[0] != '#':
                MWATable.append(line.split())
        fh.close()
        self.MWATable = np.array(MWATable, dtype=float)

    def showTables(self):
        '''Show the contents of the table. It is often for debugging'''
        print((self.MWATable))

    def getMWAValue(self, HVLMaterial, HVLValue, IntpSpace='Logrithm'):
        '''Calculate MWA for a HVL value.'''
        HVLmax=np.nan
        HVLmin=np.nan
        xcolumn=np.nan
        if HVLMaterial == 'Al':
            xcolumn = 1
            HVLmin = 2.9
            HVLmax = 20.3
        elif HVLMaterial == 'Cu':
            xcolumn = 0
            HVLmin = 0.1
            HVLmax = 5.0
        else:
            print('Incorrent HVLMaterial. Check Please!')

        if min(HVLValue)<HVLmin or max(HVLValue)>HVLmax:
            return np.nan  # just use it for out of boundary checking.
        self.xytable = np.array(self.MWATable[:,[xcolumn,2]])
        
        ## Perform cubic spline interpolation
        if IntpSpace == 'Logrithm':
            tck = intp.splrep(np.log(self.MWATable[:,xcolumn]),self.MWATable[:,2],s=0)
            result = intp.splev(np.log(HVLValue),tck,der=0)
        else:
            tck = intp.splrep(self.MWATable[:,xcolumn],self.MWATable[:,2],s=0)
            result = intp.splev(HVLValue,tck,der=0)

        ## Perform linear interpolation
        #f = intp.interp1d(self.MWATable[:,xcolumn], self.MWATable[:,2])
        #result = f(HVLValue)
        return result

#Table = MuWatAirTable("C:\Documents and Settings\lzhan\Desktop\SXT\Data\MuWatAir.dat")
#Table.showTables()
#
#x = np.linspace(np.log(0.1),np.log(5.0),100)
#x = np.exp(x)
#y = Table.getMWAValue('Cu',x)
#y1 = Table.getMWAValue('Cu',x,IntpSpace='Linear')
##print(Table.xytable)
#
#plt.figure(2)
##x = np.log(x)
##plt.plot(x,y,'r-',x,y1,'-',np.log(Table.xytable[:,0]),Table.xytable[:,1],'o')
#plt.plot(x,y,'r-',x,y1,'-',Table.xytable[:,0],Table.xytable[:,1],'o')
#plt.xlabel('HVL')
#plt.ylabel('$[(\mu^{en}_{mass})^w_{air}]_{water}$')
#plt.show()
