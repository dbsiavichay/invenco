import json, ast
from django.db import models
from providers.models import Provider
from django_pgjson.fields import JsonField
from datetime import date

class Trademark(models.Model):
	class Meta:
		ordering = ['name',]

	name = models.CharField(max_length=32)

	def __unicode__(self):
		return self.name

class Type(models.Model):
	class Meta:
		ordering = ['name',]

	name = models.CharField(max_length=32)
	#options 1: Ninguno, 2: repuesto, 3: accesorio
	usage = models.PositiveSmallIntegerField(default=1)
	specifications = JsonField(blank=True, null=True)
	print_sizes = JsonField(blank=True, null=True)

	def get_specifications(self):
		return ast.literal_eval(json.dumps(self.specifications))

	def get_print_sizes(self):
		return [float(n) for n in self.print_sizes.split(',')]

	def __unicode__(self):
		return self.name

class TypeSpecification(models.Model):
	class Meta:
		ordering = ['-when']

	name = models.CharField(max_length=128)
	when = models.CharField(max_length=32)
	options = models.CharField(max_length=128, blank=True, null=True)
	type = models.ForeignKey(Type, related_name='type_specifications')

	def __unicode__(self):
		return self.name

class Model(models.Model):
	class Meta:
		ordering = ['type', 'trademark', 'name']

	name = models.CharField(max_length=128)
	part_number = models.CharField(max_length=32, blank=True, null=True)
	specifications = JsonField(blank=True, null=True)
	type = models.ForeignKey(Type)
	trademark = models.ForeignKey(Trademark)
	replacements = models.ManyToManyField('self')

	def __unicode__(self):
		#type = self.specifications['Uso'] if self.specifications.has_key('Uso') and 'laptop' in self.specifications['Uso'].lower() else self.type
		return '%s %s' % (self.trademark, self.name)

	def get_specifications(self):
		return ast.literal_eval(json.dumps(self.specifications))

class Device(models.Model):
	class Meta:
		ordering = ['model',]

	model = models.ForeignKey(Model, verbose_name='Modelo')
	code = models.CharField(max_length=16, unique=True, verbose_name='Codigo')
	serial = models.CharField(max_length=34, unique=True, blank=True, null=True, verbose_name='Serie')
	part = models.CharField(max_length=32, blank=True, null=True, verbose_name='Parte')
	specifications = JsonField(blank=True, null=True)
	state = models.CharField(max_length=16, blank=True, null=True, verbose_name='Estado')
	provider = models.ForeignKey(Provider, blank=True, null=True, verbose_name='Proveedor')
	invoice = models.CharField(max_length=16, blank=True, null=True, verbose_name='Factura')
	date_purchase = models.DateField(blank=True, null=True, verbose_name='Compra')
	date_warranty = models.DateField(blank=True, null=True, verbose_name='Garantia')
	observation = models.TextField(blank=True, null=True, verbose_name='Observaciones')

	def get_state_icon(self):
		icon = 'glyphicon-ok-sign' if self.state == '1' else 'glyphicon-minus-sign' if self.state == '2' else 'glyphicon-remove-sign'
		return icon

	def get_timeuntil(self):
		if self.date_warranty is None:
			return ''

		now = date.today()
		delta = self.date_warranty - now

		if delta.days <= 0:
			return 'Garantia vencida'

		dmonts = delta.days/30
		days = delta.days%30
		if dmonts == 0:
			return '%s dias' % (days)

		years = dmonts/12
		months = dmonts%12

		if years == 0:
			return u'%s meses %s dias' % (months, days)

		return u'%s a\xf1os, %s meses %s dias' % (years, months, days)

	def __unicode__(self):
		return '%s | %s' % (self.model, self.code)

class Replacement(models.Model):
	model = models.ForeignKey(Model)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)
	total_price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.DecimalField(max_digits=7, decimal_places=2)
