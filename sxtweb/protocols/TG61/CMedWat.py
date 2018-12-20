import numpy as np
import scipy.interpolate as intp
from protocols.TG61.HVLAlCu import HVLAlCu
#from HVLAlCu import HVLAlCu
import os.path

class CMedWat:
    def __init__(self):
        '''Initialize the CMedWatTable by reading in data from the file specified.
            The first read in row should contains the column definition.
        '''
        FileName = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'Data/CMedWat.dat'))
        fh = open(FileName)
        LineElements = []
        self.CMWTable = []
        self.ColumnMap = {}
        for line in fh:
            line = line.strip()
            if len(line)>0 and line[0] != '#':
                self.CMWTable.append(line.split())
        fh.close()

        for i in range(len(self.CMWTable[0])): # find index for materials
            self.ColumnMap[self.CMWTable[0][i]]=i        

    def showTables(self):
        '''Show the contents of the table. It is often for debugging'''
        print((self.CMWTable))
        print('Another Table')
        print((self.ColumnMap))

    def getValue(self, HVLValue, HVLUnit, Material, IntpSpace='Logrithm'):
        '''Calculate CMW for a Material under X-ray of HVL.'''
        try:
            mi = self.ColumnMap[Material]
        except LookupError:
            print("CANNOT find the material. Check Please!")
            
        # convert HVL Unit if needed
        if (HVLUnit == 'mm Al' and HVLValue > 8.0) or \
            (HVLUnit == 'mm Cu' and HVLValue < 0.1):
            AlCu = HVLAlCu()
            tmp = AlCu.convertHVLUnit(HVLValue, HVLUnit)
            HVLValue = tmp[0]
            HVLUnit = tmp[1]

        # Note: the requirement for first element being Al or Cu excluded
        # the column head line.
        if HVLUnit == 'mm Al': # create the table for Al
            xytable = np.array([ [ self.CMWTable[i][1],self.CMWTable[i][mi] ]
                  for i in range(len(self.CMWTable))
                  if self.CMWTable[i][0]=='Al'], dtype=np.float)
        elif HVLUnit == 'mm Cu': # create the table for Cu
            xytable = np.array([ (self.CMWTable[i][1],self.CMWTable[i][mi])
                  for i in range(len(self.CMWTable))
                  if self.CMWTable[i][0]=='Cu'], dtype=np.float)
        else:
            raise LookupError('E0110') #'CMedWat: Can Not Find HVL Material'

        # self.xytable = xytable # for debugging only.

        if HVLValue<np.min(xytable[:,0]) or HVLValue>np.max(xytable[:,0]):
            raise ValueError('E0111') #'CMedWat: HVL Out of Range'
        
        ## Perform cubic spline interpolation
        if IntpSpace=='Logrithm':
            tck = intp.splrep(np.log(xytable[:,0]),xytable[:,1],s=0)
            result = intp.splev(np.log(HVLValue),tck,der=0)
        else:
            tck = intp.splrep(xytable[:,0],xytable[:,1],s=0)
            result = intp.splev(HVLValue,tck,der=0)

        ## Perform linear interpolation
        #f = intp.interp1d(xytable[:,0], xytable[:,1])
        #result = f(HVLValue)
        return result
    
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    try:
        cmw = CMedWat()
        cmw.getValue(5.1,'mm Cu', 'Lung')
    except ValueError as what:
        print(what[0])
        
#Table = CMedWatTable("C:\Documents and Settings\lzhan\Desktop\SXT\Data\CMedWat.dat")
    cmw.showTables()
##x = np.linspace(0.3,8.0,150)
    x = np.linspace(np.log(0.3),np.log(8.0),100)
    x = np.exp(x)
    y = []
    y1 = []
    for xx in x:
        y.append(cmw.getValue(xx, 'mm Al','Lung'))
        y1.append(cmw.getValue(xx, 'mm Al','Lung',IntpSpace='Linear'))
    
    plt.figure(1)
    #x = np.log(x)
    #plt.plot(x,y,'r-',x,y1,'x-',np.log(Table.xytable[:,0]),cmw.xytable[:,1],'o')
    plt.plot(x,y,'r-',x,y1,'x-',cmw.xytable[:,0],cmw.xytable[:,1],'o')
    plt.xlabel('HVL')
    plt.ylabel('$C_w^{med}$')
    plt.show()


