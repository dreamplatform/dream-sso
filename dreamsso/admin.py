
from django.contrib import admin
import django.contrib.auth.models
from django.contrib.admin.sites import AlreadyRegistered

try:
    admin.site.register(django.contrib.auth.models.Permission)
except AlreadyRegistered:
    pass

