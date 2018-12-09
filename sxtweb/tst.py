import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sxtweb.settings")

# django.setup()

from django.conf import settings

print(settings.INSTITUTE)
