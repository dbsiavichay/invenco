from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from decimal import Decimal
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.edit import ModelFormMixin
from .models import *
from .forms import * 

from stocktaking.models import Type, Equipment

class ProviderListView(ListView):
	model = Provider

class ProviderCreateView(CreateView):
	model = Provider
	fields = '__all__'
	success_url = reverse_lazy('provider_list')

class ProviderUpdateView(UpdateView):
	model = Provider
	fields = '__all__'
	success_url = reverse_lazy('provider_list')

class ProviderDeleteView(DeleteView):
	model = Provider
	success_url = reverse_lazy('invoice_list')

class InvoiceListView(ListView):
	model = Invoice

class InvoiceCreateView(CreateView):
	model = Invoice
	fields = ('provider', 'number', 'date')
	success_url = reverse_lazy('invoice_list')

	def get_context_data(self, **kwargs):
		context = super(InvoiceCreateView, self).get_context_data(**kwargs)
		formset = self.get_invoiceline_formset()
		context.update({'formset':formset})
		return context

	def form_valid(self, form):
		formset = self.get_invoiceline_formset()

		if not formset.is_valid():
			return self.form_invalid(form)

		self.object = form.save(commit=False)		
		instances = formset.save(commit=False)

		total_discount = untaxed_amount = tax_amount = total_amount = Decimal(0.0)
		for line in instances:
			tax = (line.total_price * line.iva_percent) / Decimal(100.00)
			total_discount += line.discount
			tax_amount = tax_amount + tax			
			untaxed_amount = untaxed_amount + line.total_price
			total_amount = total_amount + (tax + line.total_price)

		self.object.total_discount = total_discount
		self.object.untaxed_amount = untaxed_amount
		self.object.tax_amount = tax_amount
		self.object.total_amount = total_amount
		self.object.save()

		formset.instance = self.object
		formset.save()
		# Para repuestos y consumibles
		self.create_instances()
		##

		return redirect(self.success_url)

	# Crea instancias de repuestos y consumibles automaticamente
	def create_instances(self):
		for line in self.object.invoiceline_set.exclude(model__type__usage=Type.EQUIPMENT):
			for i in range(int(line.quantity)):
				Equipment.objects.create(model=line.model, invoice_line=line)

	def get_invoiceline_formset(self):
		post_data = self.request.POST if self.request.method == 'POST' else None
		formset = InvoiceLineFormset(post_data)
		return formset

class InvoiceUpdateView(UpdateView):
	model = Invoice
	fields = ('provider', 'number', 'date')
	success_url = reverse_lazy('invoice_list')

	def get_context_data(self, **kwargs):
		context = super(InvoiceUpdateView, self).get_context_data(**kwargs)
		formset = self.get_invoiceline_formset()
		context.update({'formset':formset})
		return context

	def form_valid(self, form):
		formset = self.get_invoiceline_formset()

		if not formset.is_valid():
			return self.form_invalid(form)

		self.object = form.save()
		formset.save()		

		untaxed_amount = tax_amount = total_amount = Decimal(0.0)		
		for line in self.object.invoiceline_set.all():
			tax = (line.total_price * line.iva_percent) / Decimal(100.00)
			tax_amount = tax_amount + tax			
			untaxed_amount = untaxed_amount + line.total_price
			total_amount = total_amount + (tax + line.total_price)

		self.object.untaxed_amount = untaxed_amount
		self.object.tax_amount = tax_amount
		self.object.total_amount = total_amount
		self.object.save()
		self.create_instances()

		return redirect(self.success_url)

	# Crea instancias de repuestos y consumibles automaticamente
	def create_instances(self):
		for line in self.object.invoiceline_set.exclude(model__type__usage=Type.EQUIPMENT):
			count = line.equipment_set.all().count()
			if int(line.quantity) > count:
				for i in range(int(line.quantity)-count):
					Equipment.objects.create(model=line.model, invoice_line=line)

	def get_invoiceline_formset(self):
		self.object = self.get_object()
		post_data = self.request.POST if self.request.method == 'POST' else None
		formset = InvoiceLineFormset(post_data, instance=self.get_object())
		return formset

class InvoiceDetailView(DetailView):
	model = Invoice

class InvoiceEquipmentsUpdateView(UpdateView):
	model = Invoice
	fields = ()
	template_name='purchases/invoice_equipments_form.html'
	success_url = reverse_lazy('invoice_list')

	def get_context_data(self, **kwargs):
		context = super(InvoiceEquipmentsUpdateView, self).get_context_data(**kwargs)
		formset = self.get_invoiceline_formset()
		context.update({'formset':formset})
		return context

	def form_valid(self, form):
		formset = self.get_invoiceline_formset()

		if not formset.is_valid():
			return self.form_invalid(form)
		formset.save()
		return redirect(self.success_url)

	def get_invoiceline_formset(self):
		self.object = self.get_object()
		post_data = self.request.POST if self.request.method == 'POST' else None
		formset = InvoiceLineEquipmentsFormset(post_data, instance=self.get_object())
		return formset