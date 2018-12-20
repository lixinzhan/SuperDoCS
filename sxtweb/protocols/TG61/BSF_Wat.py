import numpy as np
#import scipy.interpolate as intp
from io import BytesIO
import os
from protocols.TG61.HVLAlCu import HVLAlCu
from bisect import *

class BSF_Wat:
    def __init__(self):
        '''Initialize the MuWatAirTable by reading in data from the file specified.
            The first read in row should contains the column definition.
        '''
        FileName = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'Data/BSF_Wat.dat'))
        fh = open(FileName)
        self.SSD1,self.DFLD1,self.HVL1,self.HVLMaterial1, self.BwTable1 \
            = self._readFilePartTo_(fh)
        self.SSD2,self.DFLD2,self.HVL2,self.HVLMaterial2, self.BwTable2 \
            = self._readFilePartTo_(fh)
        self.SSD3,self.DFLD3,self.HVL3,self.HVLMaterial3, self.BwTable3 \
            = self._readFilePartTo_(fh)
        fh.close()

    def _readFilePartTo_(self, fh):
        linenumber = 0
        line=fh.readline().strip()
        while line != 'BEGIN':
            linenumber = linenumber + 1
            line=fh.readline().strip()

        Nentry = 3
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
            elif column[0][0:3] == 'HVL':
                HVLMaterial = column[0][4:]
                hvl = np.array(column[1].split(),dtype='f')
                Nentry = Nentry-1

        mx = len(ssd)
        my = len(fld)
        mz = len(hvl)
        thisentry = ''
        try:
            line = fh.readline().strip()
        except EOF:
            print('end of file')
        while line != 'END':
            thisentry=thisentry+' '+line
            try:
                line = fh.readline().strip()
            except EOF:
                print('End of File')

        return ssd,fld,hvl,HVLMaterial, \
               np.resize( np.genfromtxt(BytesIO(thisentry.encode()),dtype='f'),(mx,my,mz) )            

    def showTables(self):
        '''Show the contents of the table. It is often for debugging'''
        pass

    def getValue(self, SSD, DFLD, HVL, HVLUnit):
        '''Calculate Bw for a SSD, DFLD, and HVL value.'''
        
        # check HVL Unit
        if HVLUnit not in ('mm Al', 'mm Cu'):
            raise ValueError('E0103') # 'BSF_Wat: Wrong HVL Unit!'
        
        # convert HVL Unit if needed
        if (HVLUnit == 'mm Al' and HVL > 8.0) or \
            (HVLUnit == 'mm Cu' and HVL < 0.1):
            AlCu = HVLAlCu()
            tmp = AlCu.convertHVLUnit(HVL, HVLUnit)
            HVL = tmp[0]
            HVLUnit = tmp[1]
            
        if SSD<10 and HVLUnit == 'mm Al':
            tabssd = self.SSD1
            tabdfld = self.DFLD1
            tabhvl = self.HVL1
            tabbw = self.BwTable1
        elif SSD>=10 and HVLUnit == 'mm Al':
            tabssd = self.SSD2
            tabdfld = self.DFLD2
            tabhvl = self.HVL2
            tabbw = self.BwTable2
        elif SSD>=10 and HVLUnit == 'mm Cu':
            tabssd = self.SSD3
            tabdfld = self.DFLD3
            tabhvl = self.HVL3
            tabbw = self.BwTable3
        else:
            raise ValueError('E0104') # 'BSF_Wat: Value Error!'

        ##
        ## Linear interpolation using scipy but gives inconsistent result on
        ## different computers. Replaced with *manual* interpolation.
        ##
        #coord = np.resize([[[[a,b,c] for c in tabhvl] \
        #                    for b in tabdfld] \
        #                   for a in tabssd],\
        #                  (tabbw.size,3))
        #result = intp.griddata(coord,tabbw.flatten(),\
        #                       (SSD,DFLD,HVL), method='linear' )

        
        ################################################################
        # Linear interpolation in the order of SSD, HVL, and finally FLD
        ################################################################

        # make sure no strange result returned for any point out of table boundary.
        if SSD<min(tabssd) or SSD>max(tabssd):
            raise ValueError('E0100') #'BSF_Wat: SSD Out of Range!'
            #return np.nan
        if DFLD<min(tabdfld) or DFLD>max(tabdfld):
            raise ValueError('E0101') #'BSF_Wat: DFLD Out of Range!'
            #return np.nan
        if HVL<min(tabhvl) or HVL>max(tabhvl):
            raise ValueError('E0102') #'BSF_Wat: HVL Out of Range!'
            #return np.nan
                
        # make sure boundary values can be handled as well.
        if (SSD>=max(tabssd)):
            idx_ssd = bisect_left(tabssd,SSD)
        else:
            idx_ssd = bisect(tabssd,SSD)
        if (DFLD>=max(tabdfld)):
            idx_fld = bisect_left(tabdfld,DFLD)
        else:
            idx_fld = bisect(tabdfld,DFLD)
        if (HVL>=max(tabhvl)):
            idx_hvl = bisect_left(tabhvl,HVL)
        else:
            idx_hvl = bisect(tabhvl,HVL)
        
        ## Very awkard linear interpolation but works.
        ## Should be worked on later to make it more elegant.
        
        ## interpolate over SSD; lower fld bound, lower hvl
        y0 = tabbw[idx_ssd-1,idx_fld-1,idx_hvl-1]
        y1 = tabbw[idx_ssd,  idx_fld-1,idx_hvl-1]
        x0 = tabssd[idx_ssd-1]
        x1 = tabssd[idx_ssd]
        y0_ssd = y0 + (SSD-x0)*(y1-y0)/(x1-x0)
        #print x0, x1, y0, y1, y0_ssd
        ## interpolate over SSD; lower fld bound, high hvl      
        y0 = tabbw[idx_ssd-1,idx_fld-1,idx_hvl]
        y1 = tabbw[idx_ssd,  idx_fld-1,idx_hvl]
        x0 = tabssd[idx_ssd-1]
        x1 = tabssd[idx_ssd]
        y1_ssd = y0 + (SSD-x0)*(y1-y0)/(x1-x0)        
        #print x0, x1, y0, y1, y1_ssd
        ## interpolate over HVL
        x0 = tabhvl[idx_hvl-1]
        x1 = tabhvl[idx_hvl]
        y0_hvl = y0_ssd + (HVL-x0)*(y1_ssd-y0_ssd)/(x1-x0)
        #print x0, x1, y0_ssd, y1_ssd, y0_hvl

        ## interpolate over SSD; high fld bound, lower hvl
        y0 = tabbw[idx_ssd-1,idx_fld,idx_hvl-1]
        y1 = tabbw[idx_ssd,  idx_fld,idx_hvl-1]
        x0 = tabssd[idx_ssd-1]
        x1 = tabssd[idx_ssd]
        y0_ssd = y0 + (SSD-x0)*(y1-y0)/(x1-x0)
        #print x0, x1, y0, y1, y0_ssd
        ## interpolate over SSD; high fld bound, high hvl      
        y0 = tabbw[idx_ssd-1,idx_fld,idx_hvl]
        y1 = tabbw[idx_ssd,  idx_fld,idx_hvl]
        x0 = tabssd[idx_ssd-1]
        x1 = tabssd[idx_ssd]
        y1_ssd = y0 + (SSD-x0)*(y1-y0)/(x1-x0)        
        #print x0, x1, y0, y1, y1_ssd
        ## interpolate over HVL
        x0 = tabhvl[idx_hvl-1]
        x1 = tabhvl[idx_hvl]
        y1_hvl = y0_ssd + (HVL-x0)*(y1_ssd-y0_ssd)/(x1-x0)
        #print x0, x1, y0_ssd, y1_ssd, y1_hvl

        # interpolate over DFLD.        
        x0 = tabdfld[idx_fld-1]
        x1 = tabdfld[idx_fld]
        result = y0_hvl + (DFLD-x0)*(y1_hvl-y0_hvl)/(x1-x0)
        
        return result
        

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

