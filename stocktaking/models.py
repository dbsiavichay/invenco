#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.db import models
from purchases.models import Provider
from structure.models import Contributor, Department, Section
from django.contrib.auth.models import User
import reversion


@reversion.register()
class Brand(models.Model):
	class Meta:
		ordering = ['name',]

	name = models.CharField(max_length=32, unique=True, verbose_name='nombre')	

	def __unicode__(self):
		return self.name

class Type(models.Model):
	class Meta:
		ordering = ['usage','name']

	name = models.CharField(max_length=32, verbose_name='nombre')
	code = models.CharField(max_length=16, default='', verbose_name='código')
	usage = models.PositiveSmallIntegerField(default=1, verbose_name='uso')
	image = models.ImageField(upload_to='types', blank=True, null=True, verbose_name='icono')		

	def __unicode__(self):
		return self.name

class TypeSpecification(models.Model):
	class Meta:
		ordering = ['-when', 'order']

	when = models.CharField(max_length=32)
	order = models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='orden')	
	label = models.CharField(max_length=128, default='', verbose_name='nombre')
	choices = models.CharField(max_length=256, blank=True, null=True, verbose_name='choices')
	widget = models.CharField(max_length=64, blank=True, null=True)
	is_required = models.BooleanField(default=False, verbose_name='requerido?')
	type = models.ForeignKey(Type, related_name='type_specifications')

	def __unicode__(self):
		return self.name

class Set(models.Model):
	name = models.CharField(max_length=32, verbose_name='nombre')
	icon = models.ImageField(upload_to='sets',verbose_name='icono')
	types = models.ManyToManyField(Type, verbose_name='tipos')

	def __unicode__(self):
		return self.name

class SetDetail(models.Model):
	equipments = JSONField()
	owner = models.CharField(max_length=16, blank=True)
	set = models.ForeignKey(Set)

class Model(models.Model):
	class Meta:
		ordering = ['type', 'brand', 'name']

	name = models.CharField(max_length=128, verbose_name='nombre')
	part_number = models.CharField(max_length=32, blank=True, null=True, verbose_name='parte #')
	specifications = JSONField(blank=True, null=True)
	type = models.ForeignKey(Type)
	brand = models.ForeignKey(Brand, verbose_name='marca')

	def __unicode__(self):
		return '%(brand)s %(name)s' % {'brand': self.brand, 'name': self.name}

class Equipment(models.Model):
	class Meta:
		ordering = ['model',]

	STATE_CHOICES = (
		(1, 'Bueno'),
		(2, 'En reparación'),
		(3, 'Dañado'),
	)

	model = models.ForeignKey(Model, verbose_name='modelo')
	provider = models.ForeignKey(Provider, blank=True, null=True)
	code = models.CharField(max_length=16, verbose_name='código')
	serial = models.CharField(max_length=34,blank=True, verbose_name='número de serie')	
	specifications = JSONField(blank=True, null=True)
	state = models.PositiveSmallIntegerField(blank=True, null=True, choices=STATE_CHOICES, verbose_name='estado')
	invoice = models.CharField(max_length=16, blank=True, null=True)
	date_purchase = models.DateField(blank=True, null=True)
	date_warranty = models.DateField(blank=True, null=True)
	observation = models.TextField(blank=True, null=True, verbose_name='observaciones')
	in_set = models.BooleanField(default=False)
	owner = models.CharField(max_length=16, blank=True, verbose_name='propietario')

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