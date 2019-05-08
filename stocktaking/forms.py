#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from django import forms
from django.forms import ( 
	ModelForm as DjangoModelForm, Form, formset_factory, modelformset_factory,
	ModelChoiceField, ModelMultipleChoiceField, 
	CharField, IntegerField, FloatField, ChoiceField, BooleanField, FileField,
	ValidationError
)

from django.forms.widgets import HiddenInput, RadioSelect, Select
from django.forms.models import inlineformset_factory
from .models import *
from structure.models import *

from functools import partial, wraps

class TypeForm(DjangoModelForm):
	class Meta:
		model = Type
		fields = '__all__'
		widgets = {
            'usage': forms.RadioSelect,            
        }

class ModelForm(DjangoModelForm):
	class Meta:
		model = Model
		exclude = ['specifications',]
		widgets = {
			'type': HiddenInput
		}

class EquipmentForm(DjangoModelForm):
	class Meta:
		model = Equipment
		exclude = ['specifications', 'invoice_line',]
		widgets = {
			'state': RadioSelect,
		}

	def __init__(self, *args, **kwargs):
		super(EquipmentForm, self).__init__(*args, **kwargs)
		self.fields['code'].required = True
		self.fields['serial'].required = True		

class SpecificationsForm(Form):
	def __init__(self, *args, **kwargs):
		self.type = kwargs.pop('type', None)		
		self.usage = kwargs.pop('usage', None)		
		super(SpecificationsForm, self).__init__(*args, **kwargs)

		if self.type is None or self.usage is None: 
			raise ValueError('Se requiere un <tipo> y <uso>.')

		groups = self.type.groups.filter(usage=self.usage)

		for group in groups:
			self.generate_fields(group)
			
	def generate_fields(self, group):			
		for specification in group.specifications.all():			
			key = str(specification.id)
			try:
				form_field, widget = specification.field.split(':')
			except ValueError:
				form_field = specification.field
				widget = None			

			self.fields[key] = eval(form_field)(
				label = specification.name,
				required = specification.is_required,				
			)
						
			if widget: self.fields[key].widget = eval(widget)()
			if specification.choices:
				CHOICES = [(choice, choice) for choice in specification.choices.split(',')]
				self.fields[key].choices = CHOICES

			pairs = (pair.split('=') for pair in specification.attributes.split(',')) if specification.attributes is not None else None
			attrs = dict((key.strip(), eval(value.strip())) for key, value in pairs) if pairs is not None else {}
			self.fields[key].widget.attrs.update(attrs)
			self[key].group = group.name

class LocationForm(DjangoModelForm):
	equipments = ModelMultipleChoiceField(
		queryset = Equipment.objects.filter(model__type__usage=1),
		label = 'Equipos disponibles',
	)

	def __init__(self, *args, **kwargs):		
		super(LocationForm, self).__init__(*args, **kwargs)		
		self.fields['employee'].widget.choices = self.get_employee_choices()
		self.fields['department'].widget.choices = self.get_department_choices()

	def _get_employees(self):		
		employees = Employee.objects.using('sim').filter(contributor__state='ACTIVO')
		return employees	

	def get_employee_choices(self):
		choices = [('', '---------'),]		
		choices = choices + [(emp.contributor.charter, emp.contributor.charter+' | '+emp.contributor.name) for emp in self._get_employees()]		
		return choices

	def get_department_choices(self):
		choices = [('', '---------'),]		
		departments = Department.objects.using('sim').all()
		choices = choices + [(dep.code, dep.name) for dep in departments]	
		return choices

	class Meta:
		model = Location
		exclude = ['equipments',]
		widgets = {
			'employee': Select,
			'department': Select
		}

class LocationTransferForm(LocationForm):
	def __init__(self, *args, **kwargs):
		self.charter = kwargs.pop('charter', None)		
		queryset = kwargs.pop('queryset', None)		
		super(LocationTransferForm, self).__init__(*args, **kwargs)			
		if queryset is not None: self.fields['equipments'].queryset = queryset

	def clean(self):
		super(LocationTransferForm, self).clean()
		self._validate_unique = False

	def _get_employees(self):		
		queryset = super(LocationTransferForm, self)._get_employees()
		employees = queryset.exclude(contributor__charter=self.charter)
		return employees

class ReplacementForm(DjangoModelForm):
	class Meta:
		model = Replacement
		exclude = ('total_price','stock', 'inout',)

	def __init__(self, *args, **kwargs):		
		type = kwargs.pop('type', None)		

		super(ReplacementForm, self).__init__(*args, **kwargs)		

		self.fields['model'] = forms.ModelChoiceField(
			queryset=Model.objects.filter(type=type, type__usage=2),
			label='Modelo'
		)		

