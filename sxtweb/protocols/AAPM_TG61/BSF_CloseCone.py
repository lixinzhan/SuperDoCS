import numpy as np
#import scipy.interpolate as intp
from StringIO import StringIO
import os
from bisect import *

class BSF_CloseCone:
    def __init__(self):
        '''Initialize the BSF_BoneWat table by reading in data from the file specified.
        '''
        FileName = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                'Data/BSF_CloseCone.dat'))
        fh = open(FileName)
        self.FLD,self.HVL_Al,self.HVL_Cu, self.BSFTable \
            = self._readFilePartTo_(fh)

    def _readFilePartTo_(self, fh):
        linenumber = 0
        line=fh.readline().strip()
        while line <> 'BEGIN':
            linenumber = linenumber + 1
            line=fh.readline().strip()

        Nentry = 3
        while Nentry>0:
            line = fh.readline().strip()
            if len(line)==0: continue
            column = line.split(":")
            
            if column[0] == 'FLD':
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

        mx = len(fld)
        my = len(hvl_Cu)
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

        return fld,hvl_Al, hvl_Cu, \
               np.resize( np.genfromtxt(StringIO(thisentry),dtype='f'),(mx,my) )            

    def showTables(self):
        '''Show the contents of the table. It is often for debugging'''
        print self.BSFTable

    def getValue(self, DFLD, HVL, HVLUnit):
        '''Calculate Bw for a SSD, DFLD, and HVL value.'''
        
        if HVLUnit == 'mm Al':
            tabhvl = self.HVL_Al
        elif HVLUnit == 'mm Cu':
            tabhvl = self.HVL_Cu
        else:
            raise LookupError, 'E0120' #'Incorrect HVL Unit'
        
        # For out of boundary data, extropolate using their nearest neighbour.
        if HVL < np.min(tabhvl):
            HVL = np.min(tabhvl)
        elif HVL > np.max(tabhvl):
            HVL = np.max(tabhvl)
        if DFLD < np.min(self.FLD):
            DFLD = np.min(self.FLD)
        elif DFLD > np.max(self.FLD):
            DFLD = np.max(self.FLD)

        #print 'inside', DFLD, HVL

        idx_fld = bisect(self.FLD, DFLD)-1
        idx_hvl = bisect(tabhvl, HVL)-1

        #print 'inside', idx_fld, idx_hvl

        if idx_fld<len(self.FLD)-1 and (self.FLD[idx_fld]+self.FLD[idx_fld+1])/2.0<DFLD:
            idx_fld = idx_fld+1
        if idx_hvl<len(tabhvl)-1 and (tabhvl[idx_hvl]+tabhvl[idx_hvl+1])/2.0<HVL:
            idx_hvl = idx_hvl+1

        #print 'inside', idx_fld, idx_hvl

        result = self.BSFTable[idx_fld, idx_hvl]
            
        return result



#Table = BSF_CloseCone()
#Table.showTables()
#hvl=3.2
#hvl_unit='mm Cu'
#fld = 4.0 
#result = Table.getValue(fld, hvl, hvl_unit)
#print hvl, hvl_unit, fld, result
#
