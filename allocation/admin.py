from django.contrib import admin
from .models import Allocation

class AllocationAdmin(admin.ModelAdmin):
	list_display = ('employee', 'device', 'date_joined', 'is_active')

admin.site.register(Allocation, AllocationAdmin)

