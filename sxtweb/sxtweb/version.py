#
# Main, Secondary, and Minor version numbers.
#
VERSION = '2.0-Alpha2' # Version

#
# Format: DB-CALC-TEMPL
#   DB:    db model and data entry; 
#   CALC:  dose calculation algorithm,
#   TEMPL: web page layout
#
REVISION = 'D20-C100-T100'

#
# DB Schema Revision
#   Any changes in DB schema results in the DB processing during upgrade.
#   Calibration data changes will be reflected above but not here.
#   A short description of Schema change should be described here as well.
#
# 2.0: 2018-12-07
#   Big change to DB Schema. Resources, Calibration, and Calculation are fully separated.
#   It is not compatible with DB Schema 1.x any more.
# 1.2: 2012-12-20
#   Cone shape is included now. ROF is still based on Equiv. Diameter.
# 1.1: 2012-12-20
#   Added DOB for patient; Added MachineCode, FilterCode, and ConeCode for easy communication with 
#   treatment console
# 1.0: 2012-11-20
#   First creation of this entry based on Ver. 1.0b4.
#
DB_SCHEMA='2.0'

#
# Copyright Information.
#
COPYRIGHT = '(c) 2014-2018, Lixin Zhan @GRRCC'

#
# Make this unique, and don't share it with anybody.
#
SECRET_KEY = 'vb9rrx16ksa9km&amp;!dree#(cxga2etg9rsk^(56g@ntl0=pbxpn'

