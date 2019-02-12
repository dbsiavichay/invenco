# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

#from django.forms import modelformset_factory, formset_factory

from .models import *
from .forms import *

from stocktaking.models import Replacement

from pure_pagination.mixins import PaginationMixin


class FixListView(PaginationMixin, ListView):
	model = Fix
	paginate_by = 8

	def get_queryset(self):		
		queryset = super(FixListView, self).get_queryset()	
		queryset = queryset.filter(user=self.request.user)
		return queryset

class FixCreateView(CreateView):
	model = Fix
	fields = ('problem', 'solution', 'observation', 'equipment')
	success_url = '/fix/'

	def get_context_data(self, **kwargs):
		context = super(FixCreateView, self).get_context_data(**kwargs)

		#formset = self.get_formset()

		#context.update({			
		#	'formset': formset,
		#})

		return context

	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.save()

		formset = self.get_formset()

		if not formset.is_valid():
			return self.form_invalid(form)

		for frm in formset:
			last = Replacement.objects.filter(model=frm.cleaned_data['model']).order_by('-date_joined')[0]				

			if frm.cleaned_data.get('quantity') > 0:					
				rep = frm.save(commit=False)				
				rep.total_price = rep.quantity * rep.unit_price
				rep.stock = last.stock - rep.quantity				

				obs = {
					'fix_id':  self.object.id,
					'description': 'Salida por uso en arreglo.'
				}

				rep.observation = str(obs)
				rep.save()

		return redirect(self.get_success_url())

	def get_formset(self):
		ReplacementFormSet = get_replacement_formset()

		if self.request.method == 'POST':
			formset = ReplacementFormSet(self.request.POST, self.request.FILES)
		else:
			formset = ReplacementFormSet()

		return formset