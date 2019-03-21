from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.forms import modelformset_factory, formset_factory
from django.db.models import Q

from .models import *
from .forms import *
from pure_pagination.mixins import PaginationMixin

from .serializers import *

from structure.models import Employee

class ModelListView(PaginationMixin, ListView):
	model = Model
	paginate_by = 20
	template_name = 'stocktaking/model_list2.html'

	def get_queryset(self):
		import operator
		search = self.request.GET.get('search') or self.kwargs.get('search') or None		
		queryset = super(ModelListView, self).get_queryset()

		if search is None: return queryset

		fields = ['name','type__name', 'brand__name', 'part_number', 'specifications']	
		args = [Q(**{field+'__icontains': search}) for field in fields]
		queryset = self.model.objects.filter(reduce(operator.__or__, args))		

		return queryset

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

class EquipmentListView(PaginationMixin, ListView):
	model = Equipment
	#queryset = Equipment.objects.filter(in_set=False)
	queryset = Equipment.objects.all()
	paginate_by = 20
	template_name = 'stocktaking/equipment_list2.html'

	def get_context_data(self, **kwargs):
		context = super(EquipmentListView, self).get_context_data(**kwargs)
		type = self.request.GET.get('type') or self.kwargs.get('type') or None

		types = Type.objects.exclude(usage=2)
		context.update({
			#'type_id': int(type),
			'types': types
		})

		return context

	def get_queryset(self):
		import operator
		search = self.request.GET.get('search') or self.kwargs.get('search') or None		
		queryset = super(EquipmentListView, self).get_queryset()

		if search is None: return queryset

		fields = ['model__name','model__type__name', 'model__brand__name', 'model__part_number', 'code', 'serial', 'specifications']
	
		args = [Q(**{field+'__icontains': search}) for field in fields]
		charters = Employee.objects.using('sim').filter(
			Q(contributor__charter=search) | Q(contributor__name__icontains=search)
		).values_list('contributor__charter', flat=True)
		if len(charters) > 0: args.append(Q(owner__in=list(charters)))

		queryset = self.model.objects.filter(reduce(operator.__or__, args))		

		return queryset

class EquipmentModelListView(PaginationMixin, ListView):
	model = Model
	paginate_by = 10
	template_name = 'stocktaking/equipment_model_list.html'

	def get_queryset(self):
		import operator
		search = self.request.GET.get('search') or self.kwargs.get('search') or None		
		queryset = super(EquipmentModelListView, self).get_queryset()

		if search is None: return queryset

		fields = ['name','type__name', 'brand__name', 'specifications']	
		args = [Q(**{field+'__icontains': search}) for field in fields]
		queryset = self.model.objects.filter(reduce(operator.__or__, args))		

		return queryset

class EquipmentCreateView(CreateView):
	model = Equipment
	form_class = EquipmentForm2
	success_url = '/equipment/'	

	def get_context_data(self, **kwargs):
		context = super(EquipmentCreateView, self).get_context_data(**kwargs)		
		context['specifications_form'] = self.get_specification_form()

		return context

	def get_specification_form(self):
		id_type = self.request.GET.get('type') or self.kwargs.get('type') or None
		type = get_object_or_404(Type, pk=id_type)
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

class EquipmentUpdateView(UpdateView):
	model = Equipment
	form_class = EquipmentForm2
	success_url = '/equipment/'	

	def get_context_data(self, **kwargs):
		context = super(EquipmentUpdateView, self).get_context_data(**kwargs)		
		context['specifications_form'] = self.get_specification_form()

		return context

	def get_specification_form(self):
		id_type = self.request.GET.get('type') or self.kwargs.get('type') or None
		type = get_object_or_404(Type, pk=id_type)
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


class LocationListView(ListView):
	model = Location


class LocationCreateView(CreateView):
	model = Location
	fields = '__all__'








class ReplacementListView(PaginationMixin, ListView):
	model = Replacement
	paginate_by = 8

	# def get_context_data(self, **kwargs):
	# 	context = super(ReplacementListView, self).get_context_data(**kwargs)

	# 	slug = self.request.GET.get('filter') or self.kwargs.get('filter') or None

	# 	if slug is not None:
	# 		self.queryset = self.queryset.filter(model__type__usage=slug)

	# 	context.update({
	# 		'replacement_list': self.queryset,
	# 		'object_list': self.queryset,
	# 		'filter':slug
	# 	})

	# 	return context

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

# class AssignmentCreateView(CreateView):
# 	model = Assignment
# 	form_class = AssignmentForm
# 	success_url = '/equipment/'

# 	def get_context_data(self, **kwargs):
# 		context = super(AssignmentCreateView, self).get_context_data(**kwargs)		
		
# 		equipment_id = self.request.GET.get('pk') or self.kwargs.get('pk') or None
# 		#set_id = self.request.GET.get('set') or self.kwargs.get('set') or None

# 		if equipment_id is not None:
# 			equipment = Equipment.objects.get(pk=equipment_id)
# 			context['equipment'] = equipment

# 		return context

# 	def get_form_kwargs(self):
# 		kwargs = super(AssignmentCreateView, self).get_form_kwargs()
# 		equipment_id = self.request.GET.get('pk') or self.kwargs.get('pk') or None
# 		set_id = self.request.GET.get('set') or self.kwargs.get('set') or None
# 		kwargs.update({'equipment': equipment_id, 'set': set_id})
# 		return kwargs


# 	def form_valid(self, form):
# 		equipment_id = self.request.GET.get('pk') or self.kwargs.get('pk') or None

# 		equipment = Equipment.objects.get(pk=equipment_id)
# 		equipment.owner = form.cleaned_data['employee']
# 		equipment.save()

# 		return super(AssignmentCreateView, self).form_valid(form)

# 	def form_invalid(self, form):
# 		## Cuando es set no hay equipo y entra por formulario invalido
# 		set_id = self.request.GET.get('set') or self.kwargs.get('set') or None

# 		if set_id is not None:
# 			set = SetDetail.objects.get(pk=set_id)
# 			for pk in set.equipments:
# 				equipment = Equipment.objects.get(pk=pk)

# 				frmdata = form.data.copy()
# 				frmdata['equipment'] = pk				
# 				frm = AssignmentForm(frmdata)

# 				if frm.is_valid():					
# 					obj = frm.save()
					
# 					equipment.owner = frm.cleaned_data['employee']
# 					equipment.save()
# 					set.owner = frm.cleaned_data['employee']					
# 					set.save()
# 				else: 
# 					return self.render_to_response(self.get_context_data(form=form))

# 			return redirect(self.success_url)
# 		else:			
# 			return super(AssignmentCreateView, self).form_invalid(form)


# class DispatchListView(PaginationMixin, ListView):
# 	model = Replacement
# 	paginate_by = 8
# 	template_name = 'stocktaking/dispatch_list.html'
# 	queryset = Replacement.objects.order_by('model__name', '-date_joined').\
# 				distinct('model__name').filter(movement=Replacement.OUT_BY_DISPATCH)

# class DispatchCreateView(CreateView):
# 	model = Replacement
# 	#form_class = ReplacementForm
# 	fields = '__all__'
# 	template_name = 'stocktaking/dispatch_form.html'
# 	success_url = '/dispatches/'

# 	def get_context_data(self, **kwargs):
# 		context = super(DispatchCreateView, self).get_context_data(**kwargs)

# 		context['types'] = Type.objects.filter(Q(usage=2) | Q(usage=4))

# 		return context

# 	def get(self, request, *args, **kwargs):
# 		if request.is_ajax():
# 			type_id = request.GET.get('type') or kwargs.get('type') or None			
# 			type = Type.objects.get(pk=type_id)

# 			inventory = Replacement.objects.order_by('model__name', '-date_joined').\
# 				distinct('model__name').filter(model__type=type)			

# 			objects = []

# 			for replacement in inventory:
# 				objects.append({
# 					'id': replacement.model.id,
# 					'type': replacement.model.type.name,
# 					'model': str(replacement.model),
# 					'stock': replacement.stock,
# 					'properties': replacement.model.get_list_specifications()
# 				})

# 			return JsonResponse({'data':objects})
# 		else:
# 			return super(DispatchCreateView, self).get(request, *args, **kwargs)

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
	#template_name = 'stocktaking/select_type.html'
	template_name = 'stocktaking/select_type2.html'

	def get_context_data(self, **kwargs):
		context = super(SelectTypeListView, self).get_context_data()

		if 'model' in self.request.path:
			model = 'model'
		elif 'equipment' in self.request.path:			
			model = 'equipment'
			#sets = Set.objects.all()
			#context['sets'] = sets
			context['object_list'] = self.model.objects.exclude(usage=4)
		elif 'replacement' in self.request.path:
			model = 'replacement'
			context['object_list'] = self.model.objects.filter(Q(usage=2) | Q(usage=4))

		context['model'] = model

		return context