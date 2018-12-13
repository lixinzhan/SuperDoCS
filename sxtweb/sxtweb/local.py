#
# All information related to local installation.
#

import os

os.environ.setdefault('LANG','en_US')

DEBUG = True # False

ADMINS = (
    ('Lixin Zhan', 'lixinzhan@gmail.com'),
)

MANAGERS = ADMINS
CONTACTS = ADMINS


# Set SITE_ID
SITE_ID = 1
SITE_NAME = 'Grand River Regional Cancer Centre' 
INSTITUTE = SITE_NAME

ALLOWED_HOSTS = ['172.17.112.240', '192.168.17.135', '127.0.0.1', 'localhost', '[::1]' ]


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Toronto'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'


