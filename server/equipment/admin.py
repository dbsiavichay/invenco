from django.contrib import admin
from .models import Trademark, Type, TypeSpecification, Model, Device

class TrademarkAdmin(admin.ModelAdmin):
	list_display = ('name',)
	search_fields = ('name',)

class TypeSpecificationInline(admin.TabularInline):
	model = TypeSpecification

class TypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'specifications',)
	search_fields = ('name',)
	inlines = [TypeSpecificationInline,]

class ModelAdmin(admin.ModelAdmin):
	list_display = ('type', 'trademark', 'name', 'specifications',)
	search_fields = ('type', 'trademark', 'name',)

class DeviceAdmin(admin.ModelAdmin):
	list_display = ('model', 'code', 'serial', 'part', 'state', 'date_purchase', 'date_warranty', 'specifications')
	search_fields = ('code', 'serial', 'part', 'ip')
	filter_fields = ('model',)

admin.site.register(Trademark, TrademarkAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(Device, DeviceAdmin)
