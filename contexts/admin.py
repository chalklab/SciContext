""" django admin config """
from django.contrib import admin
from config.models import *


admin.site.register(Nspaces)
admin.site.register(Terms)
admin.site.register(Fields)
