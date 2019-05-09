# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.html import format_html
from django.db import models

from audit.mixins import AuditMixin

class Provider(AuditMixin, models.Model):
	ruc = models.CharField(max_length=13)
	name = models.CharField(max_length=64, verbose_name='nombre')
	representative = models.CharField(max_length=128, blank=True, null=True, verbose_name='representante legal')
	address = models.CharField(max_length=128, verbose_name='dirección')
	city = models.CharField(max_length=32, blank=True, null=True, verbose_name='ciudad')
	cellphone = models.CharField(max_length=64, blank=True, null=True, verbose_name='teléfono fijo')
	telephone = models.CharField(max_length=64, blank=True, null=True, verbose_name='celular')
	email = models.CharField(max_length=64, blank=True, null=True, verbose_name='correo electrónico')
	webpage = models.CharField(max_length=64, blank=True, null=True, verbose_name='página web')

	def __unicode__(self):
		return '%s | %s' % (self.ruc, self.name)

	class Meta:
		verbose_name = 'proveedor'
		verbose_name_plural = 'proveedores'

class Invoice(AuditMixin, models.Model):
	class Meta:
		ordering = ['-date',]

	provider = models.ForeignKey(Provider, verbose_name='proveedor')
	number = models.CharField(max_length=64, verbose_name='número de factura')
	date = models.DateField(verbose_name='fecha de factura')	
	total_discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	untaxed_amount = models.DecimalField(max_digits=10, decimal_places=2)
	tax_amount = models.DecimalField(max_digits=10, decimal_places=2)
	total_amount = models.DecimalField(max_digits=10, decimal_places=2)

	def __unicode__(self):
		return '%s|%s' % (self.number, self.provider.name)

	def get_status(self):
		status = 'Completo'
		label = 'success'
		for line in self.invoiceline_set.all():
			if line.quantity != line.equipment_set.all().count():
				status = 'Incompleto'
				label = 'danger'
							

		return format_html(
            '<span class="label label-{}">{}</span>',
            label, status,            
        )

	class Meta:
		verbose_name = 'factura'

class InvoiceLine(AuditMixin, models.Model):
	quantity = models.FloatField()
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)
	discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)	
	total_price = models.DecimalField(max_digits=10, decimal_places=2)
	iva_percent = models.DecimalField(max_digits=5, decimal_places=2, default=12)
	model = models.ForeignKey('stocktaking.Model')
	invoice = models.ForeignKey(Invoice)
	
	def __unicode__(self):
		return '%s | $%s' % (self.model.name, self.unit_price)