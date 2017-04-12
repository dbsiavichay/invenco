from django.contrib import admin
from reversion.admin import VersionAdmin
from .models import *

class BrandAdmin(admin.ModelAdmin):
    pass

admin.site.register(Brand, BrandAdmin)

