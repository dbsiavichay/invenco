# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import inlineformset_factory
from stocktaking.models import Equipment
from .models import *

class InvoiceForm(forms.ModelForm):
	class Meta:
		model = Invoice
		fields = ('provider', 'number', 'date')

	def save(self, commit=True):
	    obj = super(InvoiceForm, self).save(commit=False)
	    
	    if commit:
	        obj.save()
	    return obj

class InvoiceLineForm(forms.ModelForm):
	class Meta:
		models = Invoice		
		fields = ()

	def __init__(self, *args, **kwargs):
		from django.db.models import Q
		super(InvoiceLineForm, self).__init__(*args, **kwargs)

		self.fields['equipments'] = forms.ModelMultipleChoiceField(
			queryset = Equipment.objects.filter(model=self.instance.model).filter(
				Q(invoice_line__isnull=True) | Q(invoice_line=self.instance)
			),
			initial = self.instance.equipment_set.all(),
			required = False
		)

	def save(self, commit=True):
		for equipment in self.instance.equipment_set.all():
			equipment.invoice_line = None
			equipment.save()

		obj = super(InvoiceLineForm, self).save(commit=True)

		for equipment in self.cleaned_data['equipments']:
			equipment.invoice_line = self.instance
			equipment.save()
		
		return obj



InvoiceLineFormset = inlineformset_factory(
	Invoice, InvoiceLine, fields='__all__', min_num=1, extra=2    
)

InvoiceLineEquipmentsFormset = inlineformset_factory(
	Invoice, InvoiceLine, form=InvoiceLineForm, extra=0
)