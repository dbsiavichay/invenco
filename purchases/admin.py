from django.contrib import admin
from .models import Provider, Invoice, InvoiceLine

class ProviderAdmin(admin.ModelAdmin):
	pass

class InvoiceLineInline(admin.TabularInline):
	model = InvoiceLine

class InvoiceAdmin(admin.ModelAdmin):
	inlines = [
		InvoiceLineInline,
	]


admin.site.register(Provider, ProviderAdmin)
admin.site.register(Invoice, InvoiceAdmin)