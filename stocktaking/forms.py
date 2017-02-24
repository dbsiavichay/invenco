#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, formset_factory, modelformset_factory
from django.forms.models import inlineformset_factory
from .models import Type,TypeSpecification, Model,Equipment

from functools import partial, wraps

class TypeForm(ModelForm):
	USAGE_CHOICES = (
		(1, 'Equipo'),
		(2, 'Repuesto'),
		(3, 'Accesorio'),		
	)

	usage = forms.ChoiceField(		
		widget = forms.RadioSelect,
		choices = USAGE_CHOICES,
		label = 'Uso'
	)

	class Meta:
		model = Type
		fields = '__all__'

class TypeSpecificationInline(ModelForm):
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
				self.fields[specification.id] = forms.CharField(
					label = specification.label,
					widget = forms.NumberInput(),
					initial= initial,					
					required = specification.is_required
				)
			elif specification.widget == 'text':
				self.fields[str(specification.id)] = forms.CharField(
					label = specification.label,					
					initial= initial,
					required = specification.is_required
				)
			elif specification.widget == 'select':
				CHOICES = [(choice, choice) for choice in specification.choices.split(',')]
				CHOICES = [('', '---------')] + CHOICES
				self.fields[str(specification.id)] = forms.ChoiceField(
					label = specification.label,
					choices = CHOICES,
					initial= initial,
					required = specification.is_required					
				)
				self.fields[str(specification.id)].widget.attrs.update({'class' : 'select2'})
			elif specification.widget == 'radio':
				CHOICES = [(choice, choice) for choice in specification.choices.split(',')]
				self.fields[str(specification.id)] = forms.ChoiceField(
					label = specification.label,
					choices = CHOICES,
					initial= initial,			
					required = specification.is_required
				)
			elif specification.widget == 'checkbox':
				self.fields[str(specification.id)] = forms.BooleanField(
					label = specification.label,	
					initial= initial,				
				)
			else:
				pass

class EquipmentForm(ModelForm):

	class Meta:
		model = Equipment
		exclude = ['specifications', 'provider', 'invoice', 'date_purchase', 'date_warranty', 'owner', 'in_set']

	def __init__(self, *args, **kwargs):		
		types = kwargs.pop('types', None)		

		if types and types is not None: 
			type = types.pop(0)		

		super(EquipmentForm, self).__init__(*args, **kwargs)
		self.empty_permitted = False

		if self.instance.id is not None:
			type = self.instance.model.type.id			
		
		self.fields['model'] = forms.ModelChoiceField(
			queryset=Model.objects.filter(type=type),
			label='Modelo'
		)

		specifications = TypeSpecification.objects.filter(type = type, when='device')		

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
				)
			else:
				self.fields[key] = forms.CharField(
					label = specification.label,
					initial = 'separator',					
					required = False
				)			

		if type is not None:			
			t = Type.objects.get(pk=type)

			self.fields['title'] = forms.CharField(
				widget= forms.HiddenInput,										
				label= 'Datos de %s' % (t.name.lower(),),					
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
		return modelformset_factory(			
			Equipment,		
			form = EquipmentForm,
			extra = 0
		)