from django.contrib import admin
from .models import *

class BrandAdmin(admin.ModelAdmin):
    pass

admin.site.register(Brand, BrandAdmin)

