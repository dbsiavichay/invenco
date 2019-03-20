from django.contrib import admin
from .models import Brand, Type, Model, Group, Specification, TypeSpecification
from django.forms import formset_factory
from .forms import SpecificationsForm, TypeForm

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name',]	

class TypeAdmin(admin.ModelAdmin):
	form = TypeForm

class GroupAdmin(admin.ModelAdmin):
	pass

class SpecificationAdmin(admin.ModelAdmin):
	pass


class TypeSpecificationAdmin(admin.ModelAdmin):
	pass

admin.site.register(Brand, BrandAdmin)
admin.site.register(Type, TypeAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Specification, SpecificationAdmin)
admin.site.register(TypeSpecification, TypeSpecificationAdmin)