from django.core.management import setup_environ
from sxtweb import settings

setup_environ(settings)

from tegmine.models import *

print INSTITUTION_CODE
