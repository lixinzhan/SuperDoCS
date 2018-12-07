from django.core.management import setup_environ
from sxtweb import settings

setup_environ(settings)

from xcalc.models import *

print INSTITUTION_CODE
