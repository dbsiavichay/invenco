from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms import modelformset_factory, formset_factory
from django.db.models import Q

from .models import *
from .forms import *
from pure_pagination.mixins import PaginationMixin

from .serializers import *

class SetListView(PaginationMixin, ListView):
	model = Set
	paginate_by = 8

class SetCreateView(CreateView):
	model = Set
	fields = '__all__'
	success_url = '/set/'

	def get_context_data(self, **kwargs):
		context = super(SetCreateView, self).get_context_data(**kwargs)
		types = Type.objects.all()
		context['types'] = types

		return context

class SetUpdateView(UpdateView):
	model = Set
	fields = '__all__'
	success_url = '/set/'

class BrandListView(PaginationMixin, ListView):
	model = Brand
	paginate_by = 8

class BrandCreateView(CreateView):
	model = Brand
	fields = '__all__'
	success_url = '/brand/'

class BrandUpdateView(UpdateView):
	model = Brand
	fields = '__all__'
	success_url = '/brand/'

class BrandDeleteView(DeleteView):
	model = Brand
	success_url = '/brand/'

class TypeListView(PaginationMixin, ListView):
	model = Type
	paginate_by = 8

class TypeCreateView(CreateView):
	model = Type
	form_class = TypeForm
	success_url = '/type/'

	def get_context_data(self, **kwargs):
		context = super(TypeCreateView, self).get_context_data(**kwargs)

		if self.request.method == 'POST':			
			context['specification_form'] = TypeSpecificationInlineFormSet(self.request.POST)			
		else:			
			context['specification_form'] = TypeSpecificationInlineFormSet()

		return context

	def form_valid(self, form):
		context = self.get_context_data()
		specification_form = context['specification_form']

		if not specification_form.is_valid():
			return self.form_invalid(form)
		
		self.object = form.save()
		
		specification_form.instance = self.object
		specification_form.save()

		return redirect(self.get_success_url())
	

class TypeUpdateView(UpdateView):
	model = Type
	form_class = TypeForm
	success_url = '/type/'

	def get_context_data(self, **kwargs):
		context = super(TypeUpdateView, self).get_context_data(**kwargs)

		if self.request.method == 'POST':			
			context['specification_form'] = TypeSpecificationInlineFormSet(self.request.POST, instance=self.object)			
		else:			
			context['specification_form'] = TypeSpecificationInlineFormSet(instance=self.object)

		return context

	def form_valid(self, form):		
		context = self.get_context_data()
		specification_form = context['specification_form']

		if not specification_form.is_valid():
			return self.form_invalid(form)
		
		self.object = form.save()

		specification_form.instance = self.object
		specification_form.save()

		return redirect(self.get_success_url())
		
class TypeDeleteView(DeleteView):
	model = Type
	success_url = '/type/'

class ModelListView(PaginationMixin, ListView):
	model = Model
	paginate_by = 8

class ModelCreateView(CreateView):
	model = Model
	fields = '__all__'
	success_url = '/model/'

	def get_context_data(self, **kwargs):
		context = super(ModelCreateView, self).get_context_data(**kwargs)

		type = self.request.GET.get('type') or self.kwargs.get('type') or None

		context['type'] = type
		context['specification_form'] = self.get_specification_form(type)

		return context

	def form_valid(self, form):
		type = self.request.GET.get('type') or self.kwargs.get('type') or None
		specification_form = self.get_specification_form(type)

		if not specification_form.is_valid():
			return self.form_invalid(form)

		self.object = form.save(commit=False)
		self.object.specifications = specification_form.cleaned_data
		self.object.save()

		return redirect(self.get_success_url())

	def get_specification_form(self, type):
		if self.request.method == 'POST':			
			form = ModelSpecificationForm(self.request.POST, type = type)			
		else:
			form = ModelSpecificationForm(type = type)

		return form

class ModelUpdateView(UpdateView):
	model = Model
	fields = '__all__'
	success_url = '/model/'

	def get_context_data(self, **kwargs):
		context = super(ModelUpdateView, self).get_context_data(**kwargs)
		type = self.request.GET.get('type') or self.kwargs.get('type') or None

		context['type'] = type		
		context['specification_form'] = self.get_specification_form(type)

		return context

	def form_valid(self, form):
		type = self.request.GET.get('type') or self.kwargs.get('type') or None
		specification_form = self.get_specification_form(type)		

		if not specification_form.is_valid():
			return self.form_invalid(form)			

		self.object = form.save(commit=False)
		self.object.specifications = specification_form.cleaned_data
		self.object.save()

		return redirect(self.get_success_url())

	def get_specification_form(self, type):				
		self.object = self.get_object()		

		if self.request.method == 'POST':
			form = ModelSpecificationForm(self.request.POST, type = type, instance = self.object)
		else:
			form = ModelSpecificationForm(type = type, instance = self.object)		

		return form

class ModelDeleteView(DeleteView):
	model = Model
	success_url = '/model/'

class EquipmentListView(PaginationMixin, ListView):
	model = Equipment
	queryset = Equipment.objects.filter(in_set=False)
	paginate_by = 8

	def get_context_data(self, **kwargs):
		context = super(EquipmentListView, self).get_context_data(**kwargs)

		types = Type.objects.all()
		context.update({
			'types': types
		})

		return context

class EquipmentSetListView(PaginationMixin, ListView):
	model = SetDetail
	paginate_by = 8
	template_name = 'stocktaking/equipment_set_list.html'

class EquipmentCreateView(CreateView):
	model = Equipment
	fields = []
	success_url = '/equipment/'

	def get_context_data(self, **kwargs):
		context = super(EquipmentCreateView, self).get_context_data(**kwargs)		
		context['formset'] = self.get_formset()

		return context

	def form_valid(self, form):		
		set_id = self.request.GET.get('set') or self.kwargs.get('set') or None

		context = self.get_context_data()
		formset = context['formset']

		if not formset.is_valid():
			return self.form_invalid(form)
		
		set_equipments = []
		for form in formset:			
			if form.has_changed():
				self.object = form.save(commit=False)				
				specifications = {}
				type_specifications = form.cleaned_data['model'].type.type_specifications.filter(when='device').exclude(widget='separator')
				for ts in type_specifications:
					key = str(ts.id)
					specifications[key] = form.cleaned_data[key]

				self.object.specifications = specifications

				if set_id is not None:					
					self.object.in_set = True

				self.object.save()
				set_equipments.append(self.object.id)

		if set_id is not None:
			obj_set = Set.objects.get(pk=set_id)
			detail = SetDetail()
			detail.set = obj_set
			detail.equipments = set_equipments
			detail.save()

		return redirect(self.get_success_url())

	def get_formset(self):		
		type = self.request.GET.get('type') or self.kwargs.get('type') or None
		set = self.request.GET.get('set') or self.kwargs.get('set') or None

		post_data = self.request.POST if self.request.method == 'POST' else None

		if set is not None:
			set = Set.objects.get(pk=set)
			types = [type.id for type in set.types.all()]						
		elif type is not None:
			types = [int(type)]

		EquipmentFormSet = get_equipment_formset(types = types)			

		formset = EquipmentFormSet(post_data)		

		return formset

class EquipmentUpdateView(UpdateView):
	model = Equipment
	fields = []
	success_url = '/equipment/'

	def get_context_data(self, **kwargs):
		context = super(EquipmentUpdateView, self).get_context_data(**kwargs)		
		context['formset'] = self.get_formset()

		return context

	def form_valid(self, form):
		set_id = self.request.GET.get('pk') or self.kwargs.get('pk') or None
		type_id = self.request.GET.get('type') or self.kwargs.get('type') or None

		context = self.get_context_data()
		formset = context['formset']

		if not formset.is_valid():
			return self.form_invalid(form)
		
		for form in formset:
			if form.has_changed():
				obj = form.save(commit=False)				
				specifications = {}
				print form.cleaned_data
				if obj.owner == '':
					type_specifications = obj.model.type.type_specifications.filter(when='device').exclude(widget='separator')
				else:
					type_specifications = obj.model.type.type_specifications.exclude(when='model').exclude(widget='separator')

				for ts in type_specifications:
					key = str(ts.id)
					specifications[key] = form.cleaned_data[key]

				obj.specifications = specifications

				if set_id is not None and type_id is None:
					obj.in_set = True

				obj.save()		

		return redirect(self.get_success_url())	

	def get_formset(self):		
		type = self.request.GET.get('type') or self.kwargs.get('type') or None
		set = self.request.GET.get('pk') or self.kwargs.get('pk') or None

		post_data = self.request.POST if self.request.method == 'POST' else None
		
		if set is not None and type is not None:			
			equipment = Equipment.objects.get(pk=set)			
			instances = [(type, equipment),]
		elif set is not None:
			instances = []
			set = SetDetail.objects.get(pk=set)
			equipments = set.equipments
			for type in set.set.types.all():
				if len(equipments)>0:
					for pk in equipments:
						equipment = Equipment.objects.get(pk=pk)
						if equipment.model.type == type:
							instances.append((type.id, equipment))
							equipments.remove(pk)
				else:
					instances.append((type.id, None))	

		EquipmentFormSet = get_equipment_formset(instances = instances)
		formset = EquipmentFormSet(post_data)	

		return formset

class ReplacementListView(PaginationMixin, ListView):
	model = Replacement
	paginate_by = 8
	queryset = Replacement.objects.order_by('model__name', '-date_joined').distinct('model__name')

	def get_context_data(self, **kwargs):
		context = super(ReplacementListView, self).get_context_data(**kwargs)

		slug = self.request.GET.get('filter') or self.kwargs.get('filter') or None

		if slug is not None:
			self.queryset = self.queryset.filter(model__type__usage=slug)

		context.update({
			'replacement_list': self.queryset,
			'object_list': self.queryset,
			'filter':slug
		})

		return context

class ReplacementCreateView(CreateView):
	model = Replacement
	form_class = ReplacementForm
	success_url = '/replacement/'

	def form_valid(self, form):		
		self.object = form.save(commit=False)
		
		last = Replacement.objects.order_by('model__name', '-date_joined').distinct('model__name').filter(model=self.object.model)

		self.object.total_price = self.object.quantity * self.object.unit_price
		self.object.stock = last[0].stock + self.object.quantity if len(last) else self.object.quantity
		self.object.inout = 1
		self.object.save()

		return redirect(self.get_success_url())

	def get_form_kwargs(self):
		kwargs = super(ReplacementCreateView, self).get_form_kwargs()
		type_id = self.request.GET.get('pk') or self.kwargs.get('pk') or None		
		kwargs.update({'type': type_id})
		return kwargs

class AssignmentCreateView(CreateView):
	model = Assignment
	form_class = AssignmentForm
	success_url = '/equipment/'

	def get_context_data(self, **kwargs):
		context = super(AssignmentCreateView, self).get_context_data(**kwargs)		
		
		equipment_id = self.request.GET.get('pk') or self.kwargs.get('pk') or None
		#set_id = self.request.GET.get('set') or self.kwargs.get('set') or None

		if equipment_id is not None:
			equipment = Equipment.objects.get(pk=equipment_id)
			context['equipment'] = equipment

		return context

	def get_form_kwargs(self):
		kwargs = super(AssignmentCreateView, self).get_form_kwargs()
		equipment_id = self.request.GET.get('pk') or self.kwargs.get('pk') or None
		set_id = self.request.GET.get('set') or self.kwargs.get('set') or None
		kwargs.update({'equipment': equipment_id, 'set': set_id})
		return kwargs


	def form_valid(self, form):
		equipment_id = self.request.GET.get('pk') or self.kwargs.get('pk') or None

		equipment = Equipment.objects.get(pk=equipment_id)
		equipment.owner = form.cleaned_data['employee']
		equipment.save()

		return super(AssignmentCreateView, self).form_valid(form)

	def form_invalid(self, form):
		set_id = self.request.GET.get('set') or self.kwargs.get('set') or None

		if set_id is not None:
			set = SetDetail.objects.get(pk=set_id)
			for pk in set.equipments:
				equipment = Equipment.objects.get(pk=pk)

				form.data['equipment'] = pk				

				frm = AssignmentForm(form.data)
				if frm.is_valid():					
					obj = frm.save()
					
					equipment.owner = frm.cleaned_data['employee']
					equipment.save()
					set.owner = frm.cleaned_data['employee']					

				else: 
					return self.render_to_response(self.get_context_data(form=form))

			set.save()

			return redirect(self.success_url)
		else:			
			return super(AssignmentCreateView, self).form_invalid(form)


class DispatchListView(PaginationMixin, ListView):
	model = Replacement
	paginate_by = 8
	template_name = 'stocktaking/dispatch_list.html'
	queryset = Replacement.objects.order_by('model__name', '-date_joined').\
				distinct('model__name').filter(movement=Replacement.OUT_BY_DISPATCH)

class DispatchCreateView(CreateView):
	model = Replacement
	#form_class = ReplacementForm
	fields = '__all__'
	template_name = 'stocktaking/dispatch_form.html'
	success_url = '/dispatches/'

	def get_context_data(self, **kwargs):
		context = super(DispatchCreateView, self).get_context_data(**kwargs)

		context['types'] = Type.objects.filter(Q(usage=2) | Q(usage=4))

		return context

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			type_id = request.GET.get('type') or kwargs.get('type') or None			
			type = Type.objects.get(pk=type_id)

			inventory = Replacement.objects.order_by('model__name', '-date_joined').\
				distinct('model__name').filter(model__type=type)			

			objects = []

			for replacement in inventory:
				objects.append({
					'id': replacement.model.id,
					'type': replacement.model.type.name,
					'model': str(replacement.model),
					'stock': replacement.stock,
					'properties': replacement.model.get_list_specifications()
				})

			return JsonResponse({'data':objects})
		else:
			return super(DispatchCreateView, self).get(request, *args, **kwargs)

	# def form_valid(self, form):		
	# 	self.object = form.save(commit=False)
		
	# 	last = Replacement.objects.order_by('model__name', '-date_joined').distinct('model__name').filter(model=self.object.model)

	# 	self.object.total_price = self.object.quantity * self.object.unit_price
	# 	self.object.stock = last[0].stock + self.object.quantity if len(last) else self.object.quantity
	# 	self.object.inout = 1
	# 	self.object.save()

	# 	return redirect(self.get_success_url())

	# def get_form_kwargs(self):
	# 	kwargs = super(ReplacementCreateView, self).get_form_kwargs()
	# 	type_id = self.request.GET.get('pk') or self.kwargs.get('pk') or None		
	# 	kwargs.update({'type': type_id})
	# 	return kwargs


class SelectTypeListView(ListView):
	model = Type
	template_name = 'stocktaking/select_type.html'

	def get_context_data(self, **kwargs):
		context = super(SelectTypeListView, self).get_context_data()

		if 'model' in self.request.path:
			model = 'model'
		elif 'equipment' in self.request.path:			
			model = 'equipment'
			sets = Set.objects.all()
			context['sets'] = sets
			context['object_list'] = self.model.objects.exclude(usage=2)
		elif 'replacement' in self.request.path:
			model = 'replacement'
			context['object_list'] = self.model.objects.filter(Q(usage=2) | Q(usage=4))

		context['model'] = model

		return context