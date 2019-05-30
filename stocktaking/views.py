from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView
from django.forms import modelformset_factory, formset_factory
#from django.db.models import Q

from .models import *
from .forms import *
from .mixins import SearchMixin
from pure_pagination.mixins import PaginationMixin

#from structure.models import Employee

class SelectTypeListView(ListView):
	model = Type
	template_name = 'stocktaking/select_type.html'

	def get_context_data(self, **kwargs):
		context = super(SelectTypeListView, self).get_context_data()
		model = self.kwargs.get('model', None)
		queryset = context['object_list']
		if model == 'equipment':						
			context['object_list'] = queryset.filter(usage=Type.EQUIPMENT)
		elif model == 'replacement':			
			context['object_list'] = queryset.filter(usage=Type.REPLACEMENT)
			model = 'equipment'
		elif model == 'consumable':			
			context['object_list'] = queryset.filter(usage=Type.CONSUMABLE)
			model = 'equipment'

		context['model'] = model
		return context


class ModelListView(PaginationMixin, SearchMixin, ListView):
	model = Model
	paginate_by = 20
	search_fields = ('name', 'brand__name', 'part_number', 'specifications')	

	def get_context_data(self, **kwargs):
		context = super(ModelListView, self).get_context_data(**kwargs)
		context.update({
			'types': self.get_types()
		})
		return context

	def get_types(self):
		types = Type.objects.all()
		return types

class ModelCreateView(CreateView):
	model = Model
	form_class = ModelForm
	success_url = '/model/'	

	def get_context_data(self, **kwargs):
		context = super(ModelCreateView, self).get_context_data(**kwargs)		
		context['specifications_form'] = self.get_specifications_form()
		return context

	def form_valid(self, form):		
		specifications_form = self.get_specifications_form()
		if not specifications_form.is_valid():
			return self.form_invalid(form)

		self.object = form.save(commit=False)
		self.object.specifications = specifications_form.cleaned_data
		self.object.save()

		return redirect(self.get_success_url())

	def get_specifications_form(self):
		kwargs = {'type': self.get_type_object(), 'usage': Group.MODEL}				
		post_data = self.request.POST if self.request.method == 'POST' else None
		form = SpecificationsForm(post_data, **kwargs)
		return form

	def get_initial(self):
		kwargs = super(ModelCreateView, self).get_initial()
		kwargs.update({'type':self.get_type_object()})
		return kwargs

	def get_type_object(self):
		id_type = self.request.GET.get('type') or self.kwargs.get('type') or None
		type = get_object_or_404(Type, pk=id_type)
		return type

class ModelUpdateView(UpdateView):
	model = Model
	form_class = ModelForm
	success_url = '/model/'	

	def get_context_data(self, **kwargs):
		context = super(ModelUpdateView, self).get_context_data(**kwargs)		
		context['specifications_form'] = self.get_specifications_form()
		return context

	def form_valid(self, form):		
		specifications_form = self.get_specifications_form()		
		if not specifications_form.is_valid():
			return self.form_invalid(form)			

		self.object = form.save(commit=False)
		self.object.specifications = specifications_form.cleaned_data
		self.object.save()

		return redirect(self.get_success_url())

	def get_specifications_form(self):		
		kwargs = {'type': self.get_type_object(), 'usage': Group.MODEL}
		post_data = self.request.POST if self.request.method == 'POST' else None
		if self.request.method == 'GET':
			try:
				initials = self.object.specifications				
				kwargs.update({'initial': initials})
			except KeyError:
				pass
		form = SpecificationsForm(post_data, **kwargs)
		return form

	def get_specification_form(self, type):				
		self.object = self.get_object()		

		if self.request.method == 'POST':
			form = ModelSpecificationForm(self.request.POST, type = type, instance = self.object)
		else:
			form = ModelSpecificationForm(type = type, instance = self.object)		

		return form

	def get_type_object(self):
		id_type = self.request.GET.get('type') or self.kwargs.get('type') or None
		type = get_object_or_404(Type, pk=id_type)
		return type

class ModelDeleteView(DeleteView):
	model = Model
	success_url = '/model/'

class EquipmentListView(PaginationMixin, SearchMixin, ListView):
	model = Equipment	
	paginate_by = 20
	search_fields = ['model__name', 'model__brand__name', 'model__part_number', 'code', 'serial', 'specifications']
	queryset = model.objects.filter(model__type__usage=Type.EQUIPMENT)

	def get_context_data(self, **kwargs):		
		context = super(EquipmentListView, self).get_context_data(**kwargs)
		context.update({			
			'types': self.get_types(),
		})

		return context

	def get_types(self):
		types = Type.objects.filter(usage=Type.EQUIPMENT)
		return types

class EquipmentCreateView(CreateView):
	model = Equipment
	form_class = EquipmentForm
	success_url = '/equipment/'	

	def get_context_data(self, **kwargs):
		context = super(EquipmentCreateView, self).get_context_data(**kwargs)		
		context['specifications_form'] = self.get_specification_form()

		return context

	def get_specification_form(self):
		type = self.get_type()
		usage = Group.EQUIPMENT
		post_data = self.request.POST if self.request.method == 'POST' else None
		form = SpecificationsForm(post_data, type=type, usage=usage)
		return form

	def form_valid(self, form):		
		specifications_form = self.get_specification_form()
		if not specifications_form.is_valid():
			return self.form_invalid(form)
		
		self.object = form.save(commit=False)
		self.object.specifications = specifications_form.cleaned_data
		self.object.save()

		return redirect(self.get_success_url())

	def get_form_kwargs(self):
		kwargs = super(EquipmentCreateView, self).get_form_kwargs()
		kwargs.update({
			'type': self.get_type(),
		})
		return kwargs

	def get_type(self):
		pk = self.kwargs.get('type', None)
		type = get_object_or_404(Type, pk=pk)
		return type

class EquipmentUpdateView(UpdateView):
	model = Equipment
	form_class = EquipmentForm
	success_url = '/equipment/'	

	def get_context_data(self, **kwargs):
		context = super(EquipmentUpdateView, self).get_context_data(**kwargs)		
		context['specifications_form'] = self.get_specification_form()

		return context

	def get_specification_form(self):
		type = self.get_type()
		usage = Group.EQUIPMENT
		post_data = self.request.POST if self.request.method == 'POST' else None
		kwargs = {'type': type, 'usage': usage}
		if self.request.method == 'GET':
			try:
				initials = self.object.specifications				
				kwargs.update({'initial': initials})
			except KeyError:
				pass
		form = SpecificationsForm(post_data, **kwargs)
		return form

	def form_valid(self, form):		
		specifications_form = self.get_specification_form()
		if not specifications_form.is_valid():
			return self.form_invalid(form)

		self.object = form.save(commit=False)
		self.object.specifications = specifications_form.cleaned_data		
		self.object.save()

		return redirect(self.get_success_url())

	def get_form_kwargs(self):
		kwargs = super(EquipmentUpdateView, self).get_form_kwargs()
		kwargs.update({
			'type': self.get_type(),
		})
		return kwargs	

	def get_type(self):
		self.object = self.get_object()		
		return self.object.model.type

#Repuestos
class ReplacementListView(EquipmentListView):	
	queryset = Equipment.objects.filter(model__type__usage=Type.REPLACEMENT)
	template_name = 'stocktaking/replacement_list.html'

	def get_types(self):
		types = Type.objects.filter(usage=Type.REPLACEMENT)
		return types

class ReplacementStockView(ModelListView):	
	template_name = 'stocktaking/replacement_stock.html'
	queryset = Model.objects.filter(type__usage=Type.REPLACEMENT)

	def get_types(self):
		types = Type.objects.filter(usage=Type.REPLACEMENT)
		return types

class ReplacementDeleteView(DeleteView):
	model = Equipment
	success_url = reverse_lazy('replacement_list')
###
# Consumibles
class ConsumableListView(EquipmentListView):	
	queryset = Equipment.objects.filter(model__type__usage=Type.CONSUMABLE)
	template_name = 'stocktaking/consumable_list.html'

	def get_types(self):
		types = Type.objects.filter(usage=Type.CONSUMABLE)
		return types

class ConsumableStockView(ModelListView):	
	template_name = 'stocktaking/consumable_stock.html'
	queryset = Model.objects.filter(type__usage=Type.CONSUMABLE)

	def get_types(self):
		types = Type.objects.filter(usage=Type.CONSUMABLE)
		return types

class LocationListView(ListView):
	model = Location

class LocationCreateView(CreateView):
	model = Location
	form_class = LocationForm
	success_url = reverse_lazy('location_list')

	def form_valid(self, form):
		self.object = form.save()		
		self.create_assigments(form.cleaned_data['equipments'])		
		return redirect(self.success_url)

	def create_assigments(self, equipments):
		try:		
			for eq in equipments:
				Assignment.objects.create(location=self.object, equipment=eq)				
		except:
			self.object.assignment_set.all().delete()
			self.object.delete()			
			raise Exception

class LocationTransferView(LocationCreateView):
	form_class = LocationTransferForm
	template_name = 'stocktaking/location_transfer.html'

	def get_context_data(self, **kwargs):
		context = super(LocationTransferView, self).get_context_data(**kwargs)
		context.update({'object':self.get_object()})
		return context

	def get_form_kwargs(self):
		_object = self.get_object()
		kwargs = super(LocationTransferView, self).get_form_kwargs()
		queryset = _object.equipments.filter(assignment__active=True)
		kwargs.update({
			'queryset': queryset,
			'charter': _object.employee,
			'initial': {
				'department': _object.department,
				'building':_object.building,
				'equipments': queryset.values_list('id', flat=True),
			}			
		})
		return kwargs	

	def form_valid(self, form):
		try:
			kwargs = { key: value for key, value in form.cleaned_data.items() if key != 'equipments'}			
			self.object = self.model.objects.get(**kwargs)			
		except self.model.DoesNotExist:
			self.object = form.save()
				
		equipments = form.cleaned_data['equipments']
		self.create_assigments(equipments)
		Assignment.objects.filter(location=self.get_object(), active=True, equipment__in=equipments).update(active=False)		
		return redirect(self.success_url)
