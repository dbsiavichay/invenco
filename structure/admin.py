from django.contrib import admin
from .models import Job, Department, Area, Employee

class JobAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)

class DepartmentAdmin(admin.ModelAdmin):
	list_display = ('code', 'name',)
	search_fields = ('code', 'name',)

class AreaAdmin(admin.ModelAdmin):
	list_display = ('code', 'name', 'department',)
	search_fields = ('code', 'name')
	filter_fields = ('department',)

class EmployeeAdmin(admin.ModelAdmin):
	list_display = ('user',)

admin.site.register(Job, JobAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Area, AreaAdmin)
admin.site.register(Employee, EmployeeAdmin)
