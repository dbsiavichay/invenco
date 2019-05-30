# -*- coding: utf-8 -*-
from django import forms
from django.forms import formset_factory, ModelForm, Form
from django.forms.widgets import HiddenInput
from .models import Reply

from stocktaking.models import Type, Equipment

# from functools import partial, wraps

class ReplyForm(ModelForm):
	class Meta:
		model = Reply
		exclude = ('date',)
		widgets = {
			'ticket': HiddenInput
		}

class ReplacementForm(Form):
	replacement = forms.ModelChoiceField(
		queryset = Equipment.objects.filter(
			model__type__usage=Type.REPLACEMENT,
			reply__isnull=True
		),
		label = 'Repuesto'
	)	
	serial = forms.CharField(label='Serie')

	def __init__(self, *args, **kwargs):
		type = kwargs.pop('type', None)
		super(ReplacementForm, self).__init__(*args, **kwargs)
		if type is not None:
			self.fields['replacement'].queryset = self.fields['replacement'].queryset.filter(model__type=type)		
		for key in self.fields:			
			self.fields[key].widget.attrs.update({'class': 'form-control', 'key': key})