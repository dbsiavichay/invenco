from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.db import models
from purchases.models import Provider
from structure.models import Contributor, Department, Section

class Brand(models.Model):
	class Meta:
		ordering = ['name',]

	name = models.CharField(max_length=32)

	def __unicode__(self):
		return self.name

class Type(models.Model):
	class Meta:
		ordering = ['name',]

	name = models.CharField(max_length=32)
	#usage 1: Ninguno, 2: repuesto, 3: accesorio
	usage = models.PositiveSmallIntegerField(default=1)
	specifications = JSONField(blank=True, null=True)

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
		ordering = ['type', 'brand', 'name']

	name = models.CharField(max_length=128)
	part_number = models.CharField(max_length=32, blank=True, null=True)
	specifications = JSONField(blank=True, null=True)
	type = models.ForeignKey(Type)
	brand = models.ForeignKey(Brand)
	replacements = models.ManyToManyField('self', blank=True)

	def __unicode__(self):
		return self.name

class Equipment(models.Model):
	class Meta:
		ordering = ['model',]

	model = models.ForeignKey(Model)
	provider = models.ForeignKey(Provider, blank=True, null=True)
	code = models.CharField(max_length=16, unique=True)
	serial = models.CharField(max_length=34, unique=True, blank=True, null=True)
	part = models.CharField(max_length=32, blank=True, null=True)
	specifications = JSONField(blank=True, null=True)
	state = models.CharField(max_length=16, blank=True, null=True)
	invoice = models.CharField(max_length=16, blank=True, null=True)
	date_purchase = models.DateField(blank=True, null=True)
	date_warranty = models.DateField(blank=True, null=True)
	observation = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return '%s | %s' % (self.model, self.code)

class Replacement(models.Model):
	model = models.ForeignKey(Model)
	unit_price = models.DecimalField(max_digits=10, decimal_places=2)
	total_price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.DecimalField(max_digits=7, decimal_places=2)

class Assignment(models.Model):
	class Meta:
		ordering = ['department', 'section']

	employee = models.CharField(max_length=16)
	department = models.FloatField()
	section = models.FloatField()
	date_joined = models.DateField()
	is_active = models.BooleanField()
	equipment = models.ForeignKey(Equipment)

	def responsible(self):
		contributor = Contributor.objects.using('sim').get(charter=self.employee)
		arr = contributor.name.split()
		return '%s %s' % (arr[2].capitalize(), arr[0].capitalize())