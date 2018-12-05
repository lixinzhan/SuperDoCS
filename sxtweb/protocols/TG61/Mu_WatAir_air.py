import numpy as np
import scipy.interpolate as intp
from io import StringIO
import os

class Mu_WatAir_air:
    def __init__(self):
        '''Initialize the CMedWatTable by reading in data from the file specified.
            The first read in row should contains the column definition.
        '''
        FileName = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'Data/Mu_WatAir_air.dat'))
        fh = open(FileName)
        self.MuTable = []
        for line in fh:
            line = line.strip()
            if len(line)>0 and line[0] != '#':
                self.MuTable.append(line.split())
        fh.close()

    def showTables(self):
        '''Show the contents of the table. It is often for debugging'''
        print((self.MuTable))

    def getValue(self, HVLUnit, HVLValue, IntpSpace='Logrithm'):
        '''Calculate CMW for a Material under X-ray of HVL.'''
        # Note: the requirement for first element being Al or Cu excluded
        # the column head line.
        if HVLUnit == 'mm Al': # create the table for Al
            xytable = np.array([ [ self.MuTable[i][1],self.MuTable[i][2] ]
                  for i in range(len(self.MuTable))
                  if self.MuTable[i][0]=='Al'], dtype=np.float)
        elif HVLUnit == 'mm Cu': # create the table for Cu
            xytable = np.array([ (self.MuTable[i][1],self.MuTable[i][2])
                  for i in range(len(self.MuTable))
                  if self.MuTable[i][0]=='Cu'], dtype=np.float)
        else:
            raise LookupError('Incorrect HVLUnit.')

        # self.xytable = xytable # for debugging only.
        
        ## Perform cubic spline interpolation
        if IntpSpace=='Logrithm':
            tck = intp.splrep(np.log(xytable[:,0]),xytable[:,1],s=0)
            result = intp.splev(np.log(HVLValue),tck,der=0)
        else:
            tck = intp.splrep(xytable[:,0],xytable[:,1],s=0)
            result = intp.splev(HVLValue,tck,der=0)

        return result

#Table = EabsTable("C:\Documents and Settings\lzhan\Desktop\SXT\Data\Eabs.dat")
#Table.showTables()
##x = np.linspace(0.03,8.0,150)
#x = np.linspace(-3.507,2.08,100)
#x = np.exp(x)
#y = Table.getMuValue('Al',x)
#y1= Table.getMuValue('Al',x,IntpSpace='Linear')
#
#plt.figure(1)
##x=np.log(x)
##plt.plot(x,y,'r-',x,y1,'x',np.log(Table.xytable[:,0]),Table.xytable[:,1],'o')
#plt.plot(x,y,'r-',x,y1,'x',Table.xytable[:,0],Table.xytable[:,1],'o')
#plt.xlabel('HVL')
#plt.ylabel('$\mu$')
#plt.show()


