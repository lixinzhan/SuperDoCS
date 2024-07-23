#
# Main, Secondary, and Minor version numbers.
#
VERSION = '3.1' # Version
DEVSTAGE = 'Release'  # Stage of development: Alpha, Beta, RC, Release.

#
# Format: DB-CALC-TEMPL
#   DB:    db model and data entry; 
#   CALC:  dose calculation algorithm,
#   TEMPL: web page layout
#
REVISION = 'D23-C101-T102'

#
# DB Schema Revision
#   Any changes in DB schema results in the DB processing during upgrade.
#   Calibration data changes will be reflected above but not here.
#   A short description of Schema change should be described here as well.
#
# 3.1: 2024-07-23
#   updated requirements for running under Ubuntu 22.04
#
# 3.0: 2023-05-02
#   Minor update to page display.
#
# 3.0-Alpha: 2021-10-23
#   Migrated to Django 3.2, and updated features deprecated in Django4.
#
# 2.3.1: 2021-10-22
#   Fixed issues with pip3 setup and added packaging time.
#
# 2.3: 2020-09-03
#   Changed ROF to ROF_Exposure for fixing failed SpecifyROF calculation issue.
#
# 2.2: 2019-03-31
#   Added Status to many tables including outputfactor.
#
# 2.1: 2019-01-07
#   Added Has_Pion_Ppol and DurationUnit to Calibration.
#
# 2.0: 2018-12-07
#   Big change to DB Schema. Resources, Calibration, and Calculation are fully separated.
#   It is not compatible with DB Schema 1.x any more.
#
# 1.2: 2012-12-20
#   Cone shape is included now. ROF is still based on Equiv. Diameter.
#
# 1.1: 2012-12-20
#   Added DOB for patient; Added MachineCode, FilterCode, and ConeCode for easy communication with 
#   treatment console
#
# 1.0: 2012-11-20
#   First creation of this entry based on Ver. 1.0b4.
#
DB_SCHEMA='2.3'

#
# Copyright Information.
#
COPYRIGHT = 'Copyleft 2014-2023, Lixin Zhan @GRRCC'

#
# Support Information
#
SUPPORTEMAIL = 'lixinzhan@gmail.com'


#
# Make this unique, and don't share it with anybody.
#
SECRET_KEY = 'vb9rrx16ksa9km&amp;!dree#(cxga2etg9rsk^(56g@ntl0=pbxpn'

