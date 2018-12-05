import numpy as np
import scipy.interpolate as intp
from io import StringIO
import os

class BSF_BoneWat:
    def __init__(self):
        '''Initialize the BSF_BoneWat table by reading in data from the file specified.
        '''
        FileName = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'Data/BSF_BoneWat.dat'))
        fh = open(FileName)
        self.SSD,self.FLD,self.HVL_Al,self.HVL_Cu, self.BSFTable \
            = self._readFilePartTo_(fh)

    def _readFilePartTo_(self, fh):
        linenumber = 0
        line=fh.readline().strip()
        while line != 'BEGIN':
            linenumber = linenumber + 1
            line=fh.readline().strip()

        Nentry = 4
        while Nentry>0:
            line = fh.readline().strip()
            if len(line)==0: continue
            column = line.split(":")
            
            if column[0] == 'SSD':
                ssd = np.array(column[1].split(),dtype='f')
                Nentry = Nentry-1
            elif column[0] == 'FLD':
                fld = np.array(column[1].split(),dtype='f')
                Nentry = Nentry-1
            elif column[0] == 'HVL Al':
                HVLMaterial = 'Al'
                hvl_Al = np.array(column[1].split(),dtype='f')
                Nentry = Nentry-1
            elif column[0] == 'HVL Cu':
                HVLMaterial = 'Cu'
                hvl_Cu = np.array(column[1].split(),dtype='f')
                Nentry = Nentry-1

        mx = len(ssd)
        my = len(hvl_Cu)
        mz = len(fld)
        thisentry = ''
        try:
            line = fh.readline().strip()
        except EOFError:
            print('end of file')
        while line != 'END':
            thisentry=thisentry+' '+line
            try:
                line = fh.readline().strip()
            except EOFError:
                print('End of File')

        return ssd,fld,hvl_Al, hvl_Cu, \
               np.resize( np.genfromtxt(StringIO(thisentry),dtype='f'),(mx,my,mz) )            

    def showTables(self):
        '''Show the contents of the table. It is often for debugging'''
        print(self.BSFTable)

    def getValue(self, SSD, DFLD, HVL, HVLUnit):
        '''Calculate Bw for a SSD, DFLD, and HVL value.'''
        
        if HVLUnit == 'mm Al':
            tabhvl = self.HVL_Al
        elif HVLUnit == 'mm Cu':
            tabhvl = self.HVL_Cu
        else:
            raise LookupError('E0120') #'Incorrect HVL Unit'
        
        # Table XI of TG-61 gives field size in square. The input field size
        # is in circle. Convert the circle to equivalent square to get the factor.
        FLD = np.sqrt(np.pi)*DFLD/2.0
        
        if HVL<np.min(tabhvl) or HVL>np.max(tabhvl):
            raise ValueError('E0121') #'BSF_BoneWat: HVL Out of Range'
        if FLD<np.min(self.FLD) or FLD>np.max(self.FLD):
            raise ValueError('E0122') #'BSF_BoneWat: FLD Out of Range'
        if SSD<np.min(self.SSD) or SSD>np.max(self.SSD):
            raise ValueError('E0123') #'BSF_BoneWat: SSD Out of Range'
        
        coord = np.resize([[[[a,b,c] for c in self.FLD] \
                            for b in tabhvl] \
                           for a in self.SSD],\
                          (self.BSFTable.size,3))
        result = intp.griddata(coord,self.BSFTable.flatten(),\
                               (SSD,HVL,FLD), method='linear' )
        return result



#Table = BSF_BoneWat()
##Table.showTables()
#ssd=50
#hvl=1.6
#hvl_unit='mm Al'
#fld = 1.128379177 #2.256758335
#result = Table.getValue(ssd, fld, hvl, hvl_unit)
#print ssd, hvl, hvl_unit, fld, result

#Table = BwTable("C:\Documents and Settings\lzhan\Desktop\SXT\Data\BSFWater.dat")
#x = np.linspace(10,100,20)
#y = np.linspace(1,20,20)
#z = np.linspace(0.1,5,20)
#
#xgrid=[]
#zgrid=[]
#result=[]
#for vx in x:
#    for vz in z:
#        xgrid.append(vx)
#        zgrid.append(vz)
#        result.append(Table.getBwValue(vx,10,vz,'Cu'))
#        
#print(np.resize([[xgrid[i],zgrid[i],result[i]] for i in range(len(result)) ], \
#    (len(result),3)))
#
#xgrid=np.resize(xgrid,(x.size,z.size))
#zgrid=np.resize(zgrid,(x.size,z.size))
#result=np.resize(result,(x.size,z.size))
#
#fig = plt.figure()
#ax = fig.add_subplot(111, projection='3d')
#ax.plot_surface(xgrid,zgrid,result,rstride=1,cstride=1)
#plt.show()

