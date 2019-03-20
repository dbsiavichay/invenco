#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from django import forms
from django.forms import ( 
	ModelForm as DjangoModelForm, Form, formset_factory, modelformset_factory,
	ModelChoiceField, ModelMultipleChoiceField, 
	CharField, IntegerField,FloatField, ChoiceField, BooleanField, FileField,
	ValidationError
)

from django.forms.widgets import HiddenInput, RadioSelect
from django.forms.models import inlineformset_factory
from .models import *
from structure.models import *

from functools import partial, wraps

class ModelForm(DjangoModelForm):
	class Meta:
		model = Model
		exclude = ['specifications',]
		widgets = {
			'type': HiddenInput
		}

class EquipmentForm2(DjangoModelForm):
	class Meta:
		model = Equipment
		exclude = ['specifications', 'invoice_line', 'owner']
		widgets = {
			'state': RadioSelect,
		}

	def __init__(self, *args, **kwargs):
		super(EquipmentForm2, self).__init__(*args, **kwargs)
		self.fields['state'].widget.choices.pop(0)	

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
			self[key].group = group.name
						
			if widget: self.fields[key].widget = eval(widget)()
			if specification.choices:
				CHOICES = [(choice, choice) for choice in specification.choices.split(',')]
				self.fields[key].choices = CHOICES

			pairs = (pair.split('=') for pair in specification.attributes.split(',')) if specification.attributes is not None else None
			attrs = dict((key.strip(), eval(value.strip())) for key, value in pairs) if pairs is not None else {}
			self.fields[key].widget.attrs.update(attrs)


































class TypeForm(DjangoModelForm):
	class Meta:
		model = Type
		fields = '__all__'
		widgets = {
            'usage': forms.RadioSelect,            
        }

class TypeSpecificationInline(DjangoModelForm):
	WHEN_CHOICES = (
		('model', 'Módelo'),
		('device', 'Equipo'),
		('allocation', 'Asignación'),	
	)

	WIDGET_CHICES = (
		('number', 'Número'),
		('text', 'Texto'),
		('select', 'Select'),
		('radio', 'Radio'),
		('checkbox', 'Checkbox'),
		('separator', 'Separador'),
	)

	when = forms.ChoiceField(		
		widget = forms.RadioSelect,
		choices = WHEN_CHOICES,
		label = 'Especificar en'
	)

	widget = forms.ChoiceField(		
		widget = forms.RadioSelect,
		choices = WIDGET_CHICES,
	)

	class Meta:
		model = TypeSpecification
		fields = '__all__'

TypeSpecificationInlineFormSet = inlineformset_factory(Type,
    TypeSpecification,    
    form=TypeSpecificationInline,
    extra = 1,    
)


class SetForm(DjangoModelForm):
	class Meta:
		model = Set
		exclude = ('types',)
		
class SetTypeForm(DjangoModelForm):
	class Meta:
		model = SetType
		exclude = ('set',)

SetTypeFormset = modelformset_factory(
	SetType,
    form=SetTypeForm,  
    extra = 1,
    can_delete=True    
)

class ModelSpecificationForm(forms.Form):

	def __init__(self, *args, **kwargs):
		type = kwargs.pop('type', None)
		instance = kwargs.pop('instance', None)
		
		super(ModelSpecificationForm, self).__init__(*args, **kwargs)

		specifications = TypeSpecification.objects.filter(type = type, when='model')

		for specification in specifications:
			key = str(specification.id)			
			initial = instance.specifications[key] if instance is not None and key in instance.specifications else None

			if specification.widget == 'number':
				self.fields[key] = forms.CharField(
					label = specification.label,
					widget = forms.NumberInput(),
					initial= initial,					
					required = specification.is_required
				)
			elif specification.widget == 'text':
				self.fields[key] = forms.CharField(
					label = specification.label,					
					initial= initial,
					required = specification.is_required
				)
			elif specification.widget == 'select':
				CHOICES = [(choice, choice) for choice in specification.choices.split(',')]
				CHOICES = [('', '---------')] + CHOICES
				self.fields[key] = forms.ChoiceField(
					label = specification.label,
					choices = CHOICES,
					initial= initial,
					required = specification.is_required					
				)
				self.fields[key].widget.attrs.update({'class' : 'select2'})
			elif specification.widget == 'radio':
				CHOICES = [(choice, choice) for choice in specification.choices.split(',')]
				self.fields[key] = forms.ChoiceField(
					label = specification.label,
					widget = forms.RadioSelect,
					choices = CHOICES,
					initial= initial,			
					required = specification.is_required
				)
			elif specification.widget == 'checkbox':
				self.fields[key] = forms.BooleanField(
					label = specification.label,	
					initial= initial,					
				)
			else:
				self.fields[key] = forms.CharField(
					label = specification.label,
					initial = 'separator',									
					required = False
				)

		for name, field in self.fields.items():				
			type_widget = self.fields[name].widget.__class__.__name__			
			if not type_widget == 'RadioSelect' and not type_widget == 'CheckboxInput':
				self.fields[name].widget.attrs['class'] = 'form-control' if not type_widget == 'Select' else 'select2'

class EquipmentForm(DjangoModelForm):

	class Meta:
		model = Equipment
		exclude = ['specifications', 'invoice_line', 'owner', 'in_set']

	def __init__(self, *args, **kwargs):		
		types = kwargs.pop('types', None)
		instances = kwargs.pop('instances', None)		

		if types and types is not None: 
			type = types.pop(0)

		if instances and instances is not None:
			type, instance = instances.pop(0)			
			kwargs.update({'instance': instance})

		super(EquipmentForm, self).__init__(*args, **kwargs)
		#self.empty_permitted = False		

		self.fields['model'] = forms.ModelChoiceField(
			queryset=Model.objects.filter(type=type),
			label='Modelo'
		)
		
		if self.instance.owner == '':
			specifications = TypeSpecification.objects.filter(type = type, when='device')		
		else:
			specifications = TypeSpecification.objects.filter(type = type).exclude(when='model')

		for specification in specifications:
			key = str(specification.id)
			equipment = self.instance if self.instance.id is not None else None
			initial = equipment.specifications[key] if equipment is not None and key in equipment.specifications else None

			if specification.widget == 'number':
				self.fields[key] = forms.CharField(
					label = specification.label,
					widget = forms.NumberInput(),
					initial= initial,					
					required = specification.is_required
				)
			elif specification.widget == 'text':
				self.fields[key] = forms.CharField(
					label = specification.label,					
					initial= initial,
					required = specification.is_required
				)
			elif specification.widget == 'select':
				CHOICES = [(choice, choice) for choice in specification.choices.split(',')]
				CHOICES = [('', '---------')] + CHOICES
				self.fields[key] = forms.ChoiceField(
					label = specification.label,
					choices = CHOICES,
					initial= initial,
					required = specification.is_required					
				)
				self.fields[key].widget.attrs.update({'class' : 'select2'})
			elif specification.widget == 'radio':
				CHOICES = [(choice, choice) for choice in specification.choices.split(',')]
				self.fields[key] = forms.ChoiceField(
					label = specification.label,
					widget = forms.RadioSelect,
					choices = CHOICES,
					initial= initial,			
					required = specification.is_required
				)
			elif specification.widget == 'checkbox':
				self.fields[key] = forms.BooleanField(
					label = specification.label,	
					initial= initial,
					required = False					
				)
			else:
				self.fields[key] = forms.CharField(
					label = specification.label,
					initial = 'separator',					
					required = False
				)			

		if type is not None:			
			self.fields['title'] = forms.CharField(
				widget= forms.HiddenInput,
				label= type.name.lower(),
				#label= 'Datos de %s' % (t.name.lower(),),					
				required = False
			)

		for name, field in self.fields.items():				
			type_widget = self.fields[name].widget.__class__.__name__			
			if not type_widget == 'RadioSelect' and not type_widget == 'CheckboxInput':
				self.fields[name].widget.attrs['class'] = 'form-control' if not type_widget == 'Select' else 'select2'

def get_equipment_formset(**kwargs):
	types = kwargs.get('types', None)
	instances = kwargs.get('instances', None)	

	if types is not None:
		return formset_factory(			
			wraps(EquipmentForm)(partial(EquipmentForm, types=types)),		
			extra=len(types)
		)
	else:
		return formset_factory(			
			wraps(EquipmentForm)(partial(EquipmentForm, instances=instances)),		
			extra=len(instances)
		)

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

# KardexFormSet = inlineformset_factory(
# 	Replacement, Kardex, fields='__all__',
# 	extra=1
# )

class AssignmentForm(DjangoModelForm):
	class Meta:
		model = Assignment
		fields = '__all__'	


	def __init__(self, *args, **kwargs):		
		pk = kwargs.pop('equipment', None)
		pk_set = kwargs.pop('set', None)

		equipment = Equipment.objects.get(pk = pk) if pk is not None else None

		if pk_set is not None:
			set = SetDetail.objects.get(pk = pk_set)
			equipment = Equipment.objects.get(pk=set.equipments[0])


		assignment = None
		if equipment is not None:
			history = Assignment.objects.filter(equipment=equipment, employee=equipment.owner).order_by('-date_joined')
			assignment = history[0] if len(history) else None

			
		super(AssignmentForm, self).__init__(*args, **kwargs)		

		def get_employee_choices():
			choices = [('', '---------'),]
			employees = Employee.objects.using('sim').filter(contributor__state='ACTIVO')
			for employee in employees:
				choices.append((employee.contributor.charter, employee.contributor.charter +' | ' +employee.contributor.name))

			return choices

		def get_area_choices():
			choices = [['', '---------'],]		

			departments = Department.objects.using('sim').all()
			for department in departments:
				group = [department.name,]
				choice = []
				sections = Section.objects.using('sim').filter(department=department.code)
				for section in sections:
					choice.append(['%s:%s' % (department.code, section.code), section.name])

				group.append(choice)

				choices.append(group)

			return choices

		self.fields['employee'] = forms.ChoiceField(
			choices = get_employee_choices(),		
			label = 'Empleado',
			initial = equipment.owner if equipment is not None else None
		)

		self.fields['area'] = forms.ChoiceField(
			choices = get_area_choices(),		
			label = 'Departamento/Sección',
			initial = '%s:%s' % (assignment.department, assignment.section) if assignment is not None else None
		)

		self.fields['building'] = forms.ModelChoiceField(
			queryset = Building.objects.all(),
			label = 'Edificio',
			initial = assignment.building if assignment is not None else None
		)
