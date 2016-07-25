from django.contrib import admin
from django.contrib.admin.sites import site

from core.models import *

site.register(Organization)
site.register(FieldValue)
site.register(LetterType)
site.register(Letter)
site.register(Field)
site.register(Dispatch)
site.register(Attachment)