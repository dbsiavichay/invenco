#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.postgres.fields import JSONField
from django.db import models
from purchases.models import Provider
from structure.models import *

from audit.mixins import AuditMixin

class Specification(models.Model):		
	FIELD_CHOICES = (		
		('CharField', 'Texto'),('FloatField', 'Número'),
		('ChoiceField', 'Selector'), ('ChoiceField:RadioSelect', 'RadioMultiple'),		
	)

	name = models.CharField(max_length=128, verbose_name='nombre')
	field = models.CharField(max_length=64, choices=FIELD_CHOICES, verbose_name='campo')
	attributes = models.CharField(max_length=128, blank=True, null=True, verbose_name='atributos')
	choices = models.CharField(max_length=256, blank=True, null=True, verbose_name='choices')	
	is_required = models.BooleanField(default=False, verbose_name='requerido?')	

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'especificación'
		verbose_name_plural = 'especificaciones'

class Group(models.Model):
	MODEL, EQUIPMENT = (1, 2)
	USAGE_CHOICES = ((MODEL, 'Modelo'), (EQUIPMENT, 'Equipo'),		)

	name = models.CharField(max_length=64, verbose_name='nombre')	
	usage = models.PositiveSmallIntegerField(verbose_name='uso', choices=USAGE_CHOICES) 
	specifications = models.ManyToManyField(Specification)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'grupo'

class Type(AuditMixin, models.Model):
	EQUIPMENT, REPLACEMENT, ACCESSORY, CONSUMABLE = (1,2,3,4)
	USAGE_CHOICES = (
		(EQUIPMENT, 'Equipo'),(REPLACEMENT, 'Repuesto'),(ACCESSORY, 'Accesorio'),(CONSUMABLE, 'Consumible'),
	)

	name = models.CharField(max_length=32, unique=True, verbose_name='nombre')	
	usage = models.PositiveSmallIntegerField(default=1, verbose_name='uso', choices=USAGE_CHOICES)
	image = models.ImageField(upload_to='types', blank=True, null=True, verbose_name='icono')		
	groups = models.ManyToManyField(Group, blank=True)

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'tipo'
		ordering = ['usage','name']

class Brand(AuditMixin, models.Model):
	name = models.CharField(max_length=32, unique=True, verbose_name='nombre')	

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name = 'marca'
		ordering = ['name',]

class Model(AuditMixin, models.Model):
	class Meta:
		verbose_name = 'modelo'
		ordering = ['type', 'brand', 'name']

	type = models.ForeignKey(Type, verbose_name='tipo')
	brand = models.ForeignKey(Brand, verbose_name='marca')
	name = models.CharField(max_length=128, verbose_name='nombre')
	part_number = models.CharField(max_length=32, blank=True, null=True, verbose_name='parte #')
	specifications = JSONField(blank=True, null=True)
	consumables = models.ManyToManyField('self', symmetrical=False, blank=True, verbose_name='consumibles')

	def __unicode__(self):
		return '%(brand)s %(name)s' % {'brand': self.brand, 'name': self.name}

	# def get_specifications(self):
	# 	list_specifications = []
	# 	specifications = self.type.type_specifications.exclude(widget='separator')

	# 	for specification in specifications:
	# 		key = str(specification.id)
	# 		if key in self.specifications.keys() and self.specifications[key]:				
	# 			list_specifications.append((specification.label, self.specifications[key]))

	# 	return list_specifications

	# Used for consumable_table.html component in ajax call
	def get_specifications_as_list(self):
		_list = []
		groups = self.type.groups.all()

		for group in groups:
			for specification in group.specifications.all():
				key = str(specification.id)
				if key in self.specifications.keys() and self.specifications[key]:				
					_list.append(
						'%s: %s' % (specification.name, self.specifications[key])				
					)

		return _list

	def get_replacement_count(self):
		count = self.equipment_set.filter(reply__isnull=True).exclude(state=10).count();
		return count

	def get_available_consumable_list(self):
		queryset = self.equipment_set.filter(reply__isnull=True)
		return queryset

	def get_consumable_stock(self):
		count = self.get_available_consumable_list().count()
		return count

class Equipment(models.Model):	
	STATE_CHOICES = (
		(1, 'Bueno'),
		(2, 'Regular'),
		(3, 'En reparación'),
		(10, 'Dañado'),
	)

	model = models.ForeignKey(Model, verbose_name='modelo')	
	code = models.CharField(max_length=16, blank=True, null=True, verbose_name='código')
	serial = models.CharField(max_length=34, blank=True, null=True, verbose_name='número de serie')	
	specifications = JSONField(blank=True, null=True)
	state = models.PositiveSmallIntegerField(default=1, choices=STATE_CHOICES, verbose_name='estado')	
	date = models.DateTimeField(auto_now_add=True)
	observation = models.TextField(blank=True, null=True, verbose_name='observaciones')
	reply = models.ForeignKey('maintenance.Reply', blank=True, null=True, related_name='replacements')
	invoice_line = models.ForeignKey('purchases.InvoiceLine', blank=True, null=True)

	def __unicode__(self):
		representation =  '%s | %s | %s' % (self.model, self.code, self.serial)
		responsible = self.get_responsible()
		representation = '%s | %s' % (representation, responsible) if responsible else representation
		return representation 

	def get_responsible(self):
		try:
			assignment = self.assignment_set.get(active=True)
			return assignment.location.get_employee()
		except:
			return ''

	def get_department(self):
		try:
			assignment = self.assignment_set.get(active=True)
			return assignment.location.get_department()
		except:
			return ''

	# def get_list_specifications(self):
	# 	list_specifications = []
	# 	specifications = self.model.type.type_specifications.exclude(widget='separator')

	# 	for specification in specifications:
	# 		key = str(specification.id)
	# 		if key in self.specifications.keys():				
	# 			list_specifications.append(
	# 				'%s: %s' % (specification.label, self.specifications[key])				
	# 			)

	# 	return list_specifications

	def get_state(self):		
		return dict(self.STATE_CHOICES).get(self.state) if self.state else ''

	class Meta:
		verbose_name = 'equipo'
		ordering = ['model',]

class Location(models.Model):
	class Meta:
		ordering = ['department',]
		unique_together = ['employee', 'department', 'building']	

	employee = models.CharField(max_length=16, verbose_name='empleado')
	department = models.FloatField(verbose_name='departamento')	
	building = models.ForeignKey(Building, blank=True, null=True, verbose_name='edificio')
	equipments = models.ManyToManyField(Equipment, through='Assignment', verbose_name='equipos disponibles')

	def __unicode__(self):
		return '%s, %s' % (self.building, self.get_employee())

	def get_department(self):
		department = Department.objects.using('sim').get(code=self.department)
		return department.name


	def get_employee(self):
		contributor = Contributor.objects.using('sim').get(charter=self.employee)
		arr = contributor.name.split()
		return '%s %s' % (arr[2], arr[0])

class Assignment(models.Model):
	location = models.ForeignKey(Location)
	equipment = models.ForeignKey(Equipment)
	date = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

class Dispatch(models.Model):
	employee = models.CharField(max_length=16, verbose_name='solicitante')
	observation = models.TextField(blank=True, null=True, verbose_name='observaciones')
	date = models.DateTimeField(auto_now_add=True)
	replies = models.ManyToManyField('maintenance.Reply')

	def get_employee(self):
		contributor = Contributor.objects.using('sim').get(charter=self.employee)
		arr = contributor.name.split()
		return '%s %s' % (arr[2], arr[0])

	def get_details(self):
		result = {}
		args = (
			'ticket__equipment__model__type__name', 'ticket__equipment__model__brand__name', 'ticket__equipment__model__name', 'ticket__equipment__code', 'ticket__equipment__serial',
			'replacements__model__type__name', 'replacements__model__brand__name', 'replacements__model__name'
		)
		queryset = self.replies.values(*args).annotate(num=models.Count('replacements__model'))
		for data in queryset:
			key = '{} {} {}|{}|{}'.format(data[args[0]], data[args[1]], data[args[2]], data[args[3]], data[args[4]])
			description = '{} {} {}'.format(data[args[5]], data[args[6]], data[args[7]])
			quantity = data['num']
			if key in result:
				result[key].append((description, quantity))
			else:
				result[key] = [(description, quantity),]

		return result

	class Meta:
		ordering = ('-date', )