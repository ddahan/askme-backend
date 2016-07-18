from django.contrib import admin
from django.contrib.admin.sites import site
from django.contrib.auth import get_user_model

from profiles.models import Customer

User = get_user_model()

# Register your models here.
site.register(User)
site.register(Customer)
