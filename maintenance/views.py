# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

#from django.forms import modelformset_factory, formset_factory

from .models import *
from .forms import *

from stocktaking.models import KardexReplacement

from pure_pagination.mixins import PaginationMixin


class FixListView(PaginationMixin, ListView):
	model = Fix
	paginate_by = 8

class FixCreateView(CreateView):
	model = Fix
	fields = '__all__'
	success_url = '/fix/'

	def get_context_data(self, **kwargs):
		context = super(FixCreateView, self).get_context_data(**kwargs)

		formset = self.get_formset()

		context.update({			
			'formset': formset,
		})

		return context

	def form_valid(self, form):
		fix = form.save()

		formset = self.get_formset()

		if formset.is_valid():
			for frm in formset:
				last = KardexReplacement.objects.filter(model=frm.cleaned_data['model']).order_by('-date_joined')[0]				

				if frm.cleaned_data.get('quantity') > 0:					
					rep = frm.save(commit=False)				
					rep.total_price = rep.quantity * rep.unit_price
					rep.stock = last.stock - rep.quantity				

					obs = {
						'fix_id':  fix.id,
						'description': 'Salida por uso en arreglo.'
					}

					rep.observation = str(obs)
					rep.save()
		else:
			return super(FixCreateView, self).form_invalid(form)

		return redirect(self.success_url)

	def get_formset(self):
		ReplacementFormSet = get_replacement_formset()

		if self.request.method == 'POST':
			formset = ReplacementFormSet(self.request.POST, self.request.FILES)
		else:
			formset = ReplacementFormSet()

		return formset