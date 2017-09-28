#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.db import models
from purchases.models import Provider
from structure.models import *
from django.contrib.auth.models import User

from audit.mixins import AuditMixin

class Brand(AuditMixin, models.Model):
	class Meta:
		ordering = ['name',]

	name = models.CharField(max_length=32, unique=True, verbose_name='nombre')	

	def __unicode__(self):
		return self.name

class Type(AuditMixin, models.Model):
	class Meta:
		ordering = ['usage','name']

	USAGE_CHOICES = (
		(1, 'Equipo'),
		(2, 'Repuesto'),
		(3, 'Accesorio'),
		(4, 'Consumible'),
	)

	name = models.CharField(max_length=32, unique=True, verbose_name='nombre')
	code = models.CharField(max_length=16, unique=True, verbose_name='código')
	usage = models.PositiveSmallIntegerField(default=1, verbose_name='uso', choices=USAGE_CHOICES)
	image = models.ImageField(upload_to='types', blank=True, null=True, verbose_name='icono')		

	def __unicode__(self):
		return self.name

class TypeSpecification(AuditMixin, models.Model):
	class Meta:
		ordering = ['-when', 'order']

	when = models.CharField(max_length=32)
	order = models.PositiveSmallIntegerField(verbose_name='orden')	
	label = models.CharField(max_length=128, verbose_name='nombre')
	choices = models.CharField(max_length=256, blank=True, null=True, verbose_name='choices')
	widget = models.CharField(max_length=64)
	is_required = models.BooleanField(default=False, verbose_name='requerido?')
	type = models.ForeignKey(Type, related_name='type_specifications')

	def __unicode__(self):
		return self.label

class Set(AuditMixin, models.Model):
	name = models.CharField(max_length=32, unique=True, verbose_name='nombre')
	icon = models.ImageField(upload_to='sets',verbose_name='icono')	
	types = models.ManyToManyField(Type, through='SetType', verbose_name='tipos')


	def __unicode__(self):
		return self.name

class SetType(AuditMixin, models.Model):
	class Meta:
		ordering = ('order',)

	is_primary = models.BooleanField(default=False)
	order = models.PositiveSmallIntegerField()
	set = models.ForeignKey(Set)
	type = models.ForeignKey(Type)

class SetDetail(AuditMixin, models.Model):
	class Meta:
		ordering = ['-date']

	equipments = JSONField(verbose_name='equipos')
	owner = models.CharField(max_length=16, blank=True, null=True, verbose_name='propietario')
	date = models.DateTimeField(auto_now_add=True)
	set = models.ForeignKey(Set)

	def __unicode__(self):
		return ','.join(str(i) for i in self.equipments)

	def get_responsible(self):
		contributor = Contributor.objects.using('sim').get(pk=self.owner)
		return contributor.name

class Model(AuditMixin, models.Model):
	class Meta:
		ordering = ['type', 'brand', 'name']

	name = models.CharField(max_length=128, verbose_name='nombre')
	part_number = models.CharField(max_length=32, blank=True, null=True, verbose_name='parte #')
	specifications = JSONField(blank=True, null=True)
	type = models.ForeignKey(Type, verbose_name='tipo')
	brand = models.ForeignKey(Brand, verbose_name='marca')

	def __unicode__(self):
		return '%(brand)s %(name)s' % {'brand': self.brand, 'name': self.name}

	def get_specifications(self):
		list_specifications = []
		specifications = self.type.type_specifications.exclude(widget='separator')

		for specification in specifications:
			key = str(specification.id)
			list_specifications.append((specification.label, self.specifications[key]))

		return list_specifications

	def get_list_specifications(self):
		list_specifications = []
		specifications = self.type.type_specifications.exclude(widget='separator')

		for specification in specifications:
			key = str(specification.id)
			list_specifications.append(
				'%s: %s' % (specification.label, self.specifications[key])				
			)

		return list_specifications


class Equipment(AuditMixin, models.Model):
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
	serial = models.CharField(max_length=34, verbose_name='número de serie')	
	specifications = JSONField(blank=True, null=True)
	state = models.PositiveSmallIntegerField(blank=True, null=True, choices=STATE_CHOICES, verbose_name='estado')
	invoice = models.CharField(max_length=16, blank=True, null=True)
	date_purchase = models.DateField(blank=True, null=True)
	date_warranty = models.DateField(blank=True, null=True)
	date = models.DateTimeField(auto_now_add=True)
	observation = models.TextField(blank=True, null=True, verbose_name='observaciones')
	owner = models.CharField(max_length=16, blank=True, verbose_name='propietario')
	in_set = models.BooleanField(default=False)

	def __unicode__(self):
		representation =  '%s | %s' % (self.model, self.code)
		responsible = self.get_responsible()
		representation = '%s | %s' % (representation, responsible) if responsible else representation

		return representation 

	def get_responsible(self):
		if not self.owner:
			return ''

		contributor = Contributor.objects.using('sim').get(pk=self.owner)
		return contributor.name

	def get_location(self):
		if not self.owner:
			return ''

		assignments = Assignment.objects.filter(employee=self.owner).order_by('-date_joined')
		ass = assignments[0].building.name


	def get_list_specifications(self):
		list_specifications = []
		specifications = self.model.type.type_specifications.exclude(widget='separator')

		for specification in specifications:
			key = str(specification.id)
			if key in self.specifications.keys():				
				list_specifications.append(
					'%s: %s' % (specification.label, self.specifications[key])				
				)

		return list_specifications

class Assignment(AuditMixin, models.Model):
	class Meta:
		ordering = ['department', 'section', '-date_joined']	

	employee = models.CharField(max_length=16, verbose_name='empleado')
	department = models.FloatField(verbose_name='departamento')
	section = models.FloatField(verbose_name='sección')
	date_joined = models.DateTimeField(auto_now_add=True)	
	equipment = models.ForeignKey(Equipment)
	building = models.ForeignKey(Building, blank=True, null=True, verbose_name='edificio')

	def __unicode__(self):
		return '%s, %s' % (self.equipment, self.responsible())

	def responsible(self):
		contributor = Contributor.objects.using('sim').get(charter=self.employee)
		arr = contributor.name.split()
		return '%s %s' % (arr[2], arr[0])

class Replacement(AuditMixin, models.Model):
	IN_BY_INITIAL = 1
	IN_BY_PURCHASE = 2
	OUT_BY_FIX = 5
	OUT_BY_DISPATCH = 6

	MOVEMENT_CHOICES = (
		(IN_BY_INITIAL, 'Entrada por levantamiento inicial'),
		(IN_BY_PURCHASE, 'Entrada por compra'),
		(OUT_BY_FIX, 'Salida por reparación'),
		(OUT_BY_DISPATCH, 'Salida por despacho'),
	)

	quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='cantidad')
	unit_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='precio unitario')
	total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='precio total')
	stock = models.DecimalField(max_digits=10, decimal_places=2)
	observation = models.TextField(blank=True, null=True, verbose_name='Observaciones')
	movement = models.PositiveSmallIntegerField(choices=MOVEMENT_CHOICES)
	date_joined = models.DateTimeField(auto_now_add=True)
	model = models.ForeignKey(Model)

	def __unicode__(self):
		return '%s | %s' % (self.model, self.stock)

	