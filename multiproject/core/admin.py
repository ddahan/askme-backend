from django.contrib import admin
from django.contrib.admin.sites import site

from core.models import *

site.register(Address)
site.register(Organization)
site.register(Format)
site.register(Zone)
site.register(FieldValue)
site.register(LetterType)
site.register(ZoneText)
site.register(Letter)
site.register(Field)
site.register(Dispatch)
site.register(Attachment)