from django.contrib import admin
from .models import *

class InvoiceLineInline(admin.TabularInline):
	model = InvoiceLine

class InvoiceAdmin(admin.ModelAdmin):
	inlines = [
		InvoiceLineInline,
	]


admin.site.register(Invoice, InvoiceAdmin)