from django.test import TestCase
from protocols.AAPM_TG61.BSF_Wat import BSF_Wat
from protocols.AAPM_TG61.BSF_CloseCone import BSF_CloseCone
from math import *

class BSF_Wat_Test(TestCase):
        
    def test_boundary(self):        
        bsf = BSF_Wat()
        
        #
        # success cases
        #
        
        # case 1
        self.assertAlmostEqual(bsf.getValue(SSD=1.5, DFLD=1.0, HVL=0.04, HVLUnit='mm Al'),
                               1.001)        
        # case 2
        self.assertAlmostEqual(bsf.getValue(SSD=1.5, DFLD=20.0, HVL=4.0, HVLUnit='mm Al'),
                               1.133)
        # case 3
        self.assertAlmostEqual(bsf.getValue(SSD=3.0, DFLD=1.0, HVL=4.0, HVLUnit='mm Al'),
                               1.058)
        # case 4
        self.assertAlmostEqual(bsf.getValue(SSD=10.0, DFLD=1.0, HVL=0.04, HVLUnit='mm Al'),
                               1.006)
        # case 5
        self.assertAlmostEqual(bsf.getValue(SSD=30.0, DFLD=1.0, HVL=8.0, HVLUnit='mm Al'),
                               1.053)
        # case 6
        self.assertAlmostEqual(bsf.getValue(SSD=30.0, DFLD=20.0, HVL=1.0, HVLUnit='mm Al'),
                               1.169)
        # case 7
        self.assertAlmostEqual(bsf.getValue(SSD=50.0, DFLD=20.0, HVL=0.5, HVLUnit='mm Al'),
                               1.094)
        # case 8
        self.assertAlmostEqual(bsf.getValue(SSD=100.0, DFLD=20.0, HVL=0.04, HVLUnit='mm Al'),
                               1.006)
        # case 9
        self.assertAlmostEqual(bsf.getValue(SSD=100.0, DFLD=20.0, HVL=8.0, HVLUnit='mm Al'),
                               1.508)
        # case 10
        self.assertAlmostEqual(bsf.getValue(SSD=10.0, DFLD=1.0, HVL=0.1, HVLUnit='mm Cu'),
                               1.062)
        # case 11
        self.assertAlmostEqual(bsf.getValue(SSD=10.0, DFLD=1.0, HVL=5.0, HVLUnit='mm Cu'),
                               1.017)
        # case 12
        self.assertAlmostEqual(bsf.getValue(SSD=50.0, DFLD=20.0, HVL=0.5, HVLUnit='mm Cu'),
                               1.499)
        # case 13
        self.assertAlmostEqual(bsf.getValue(SSD=50.0, DFLD=1.0, HVL=5.0, HVLUnit='mm Cu'),
                               1.018)
        # case 14
        self.assertAlmostEqual(bsf.getValue(SSD=50.0, DFLD=10.0, HVL=1.0, HVLUnit='mm Cu'),
                               1.344)
        # case 15
        self.assertAlmostEqual(bsf.getValue(SSD=100.0, DFLD=5.0, HVL=2.0, HVLUnit='mm Cu'),
                               1.167, 6)
        # case 16
        self.assertAlmostEqual(bsf.getValue(SSD=100.0, DFLD=20.0, HVL=5.0, HVLUnit='mm Cu'),
                               1.237)

        #
        # failure cases
        #
        
        # case 1
        self.assertRaisesRegexp(ValueError, 'E0100',
                                bsf.getValue,SSD=1.49, DFLD=10.0, HVL=1.0, HVLUnit='mm Al')
        # case 2
        self.assertRaisesRegexp(ValueError, 'E0101',
                                bsf.getValue,SSD=10.0, DFLD=0.99, HVL=1.0, HVLUnit='mm Al')
        # case 3
        self.assertRaisesRegexp(ValueError, 'E0102',
                                bsf.getValue,SSD=10.0, DFLD=10.0, HVL=0.039, HVLUnit='mm Al')
        # case 4
        self.assertRaisesRegexp(ValueError, 'E0103',
                                bsf.getValue,SSD=10.0, DFLD=10.0, HVL=1.0, HVLUnit='mm A')
        # case 5
        self.assertRaisesRegexp(ValueError, 'E0102',
                                bsf.getValue,SSD=9.99, DFLD=10.0, HVL=4.01, HVLUnit='mm Al')
        ## case 6   # automatically convert mm Al to mm Cu. Not exception raised.
        #self.assertRaisesRegexp(ValueError, 'E0103',
        #                        bsf.getValue,SSD=20.0, DFLD=10.0, HVL=8.01, HVLUnit='mm Al')
        # case 7
        self.assertRaisesRegexp(ValueError, 'E0100',
                                bsf.getValue,SSD=100.01, DFLD=10.0, HVL=1.0, HVLUnit='mm Al')
        # case 8
        self.assertRaisesRegexp(ValueError, 'E0101',
                                bsf.getValue,SSD=50.0, DFLD=23.1, HVL=1.0, HVLUnit='mm Al')
        # case 9
        self.assertRaisesRegexp(ValueError, 'E0102',
                                bsf.getValue,SSD=50.0, DFLD=10.0, HVL=0.039, HVLUnit='mm Al')
        ## case 10 # automatic HVL unit convert. No error raised
        #self.assertRaisesRegexp(ValueError, 'E0102',
        #                        bsf.getValue,SSD=50.0, DFLD=10.0, HVL=8.01, HVLUnit='mm Al')
        # case 11
        self.assertRaisesRegexp(ValueError, 'E0104',
                                bsf.getValue,SSD=9.99, DFLD=10.0, HVL=0.5, HVLUnit='mm Cu')
        # case 12
        self.assertRaisesRegexp(ValueError, 'E0101',
                                bsf.getValue,SSD=50.0, DFLD=0.99, HVL=0.5, HVLUnit='mm Cu')
        # case 13
        self.assertRaisesRegexp(ValueError, 'E0101',
                                bsf.getValue,SSD=50.0, DFLD=23.1, HVL=0.5, HVLUnit='mm Cu')
        ## case 14 # automatic HVL unit conversion. No error raised.
        #self.assertRaisesRegexp(ValueError, 'E0102',
        #                        bsf.getValue,SSD=50.0, DFLD=10.0, HVL=0.09, HVLUnit='mm Cu')
        # case 15
        self.assertRaisesRegexp(ValueError, 'E0102',
                                bsf.getValue,SSD=50.0, DFLD=10.0, HVL=5.01, HVLUnit='mm Cu')
        # case 16
        self.assertRaisesRegexp(ValueError, 'E0103',
                                bsf.getValue,SSD=50.0, DFLD=10.0, HVL=1.0, HVLUnit='mm C')
        
    def test_interpolation(self):
        bsf = BSF_Wat()
        
        # case 1
        self.assertAlmostEqual(bsf.getValue(SSD=50.0, DFLD=11.284, HVL=0.55, HVLUnit='mm Cu'),
                               1.393402, 6)


class BSF_CloseCone_Test(TestCase):
        
    def test_boundary(self):        
        bsf = BSF_CloseCone()

        self.assertAlmostEqual(bsf.getValue( 4.0, 0.2, 'mm Cu'), 1.006, 6)
        self.assertAlmostEqual(bsf.getValue( 4.5, 0.5, 'mm Cu'), 1.006, 6)
        self.assertAlmostEqual(bsf.getValue( 4.5, 3.0, 'mm Cu'), 1.004, 6)
        self.assertAlmostEqual(bsf.getValue( 4.5, 3.3, 'mm Cu'), 1.004, 6)
        self.assertAlmostEqual(bsf.getValue( 4.6, 0.2, 'mm Cu'), 1.006, 6)
        self.assertAlmostEqual(bsf.getValue( 4.6, 0.6, 'mm Cu'), 1.006, 6)
        self.assertAlmostEqual(bsf.getValue( 7.8, 1.2, 'mm Cu'), 1.007, 6)
        self.assertAlmostEqual(bsf.getValue(22.6, 0.5, 'mm Cu'), 1.011, 6)
        self.assertAlmostEqual(bsf.getValue(23.0, 3.2, 'mm Cu'), 1.008, 6)
        self.assertAlmostEqual(bsf.getValue(17.0, 0.9, 'mm Cu'), 1.010, 6)

