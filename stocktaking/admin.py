from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import *

@admin.register(Brand)
class BrandAdmin(VersionAdmin):
    pass

