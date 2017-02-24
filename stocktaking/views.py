from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from django.forms import modelformset_factory, formset_factory
from django.utils.encoding import force_unicode
from rest_framework import viewsets
from .views import *
from .models import *
from .forms import *
from pure_pagination.mixins import PaginationMixin

from .serializers import *

class AuditMixin(object):    
    def form_valid(self, form):
		ACTION = ADDITION if form.instance.id is None else CHANGE

		self.object = form.save()
		LogEntry.objects.log_action(
		    user_id         = self.request.user.id, 
		    content_type_id = ContentType.objects.get_for_model(self.object).id,
		    object_id       = self.object.id,
		    object_repr     = force_unicode(self.object), 
		    action_flag     = ACTION
		)
		return super(AuditMixin, self).form_valid(form)

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
		
		if specification_form.is_valid():
			self.object = form.save()
			specification_form.instance = self.object
			specification_form.save()
			return redirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form))

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
		
		if specification_form.is_valid():
			self.object = form.save()
			specification_form.instance = self.object
			specification_form.save()
			return redirect(self.get_success_url())
		else:
			return self.render_to_response(self.get_context_data(form=form))

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
			return super(ModelCreateView, self).form_invalid(form)

		self.object = form.save(commit=False)
		self.object.specifications = specification_form.cleaned_data

		return super(ModelCreateView, self).form_valid(form)

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
			return super(ModelUpdateView, self).form_invalid(form)			

		self.object = form.save(commit=False)
		self.object.specifications = specification_form.cleaned_data

		return super(ModelUpdateView, self).form_valid(form)


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
		context['sets'] = SetDetail.objects.all()

		return context

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
		if formset.is_valid():
			set_equipments = []
			for form in formset:
				obj = form.save(commit=False)				
				specifications = {}
				type_specifications = form.cleaned_data['model'].type.type_specifications.filter(when='device').exclude(widget='separator')
				for ts in type_specifications:
					key = str(ts.id)
					specifications[key] = form.cleaned_data[key]

				obj.specifications = specifications
				if set_id is not None:					
					obj.in_set = True

				obj.save()
				set_equipments.append(obj.id)

			if set_id is not None:
				obj_set = Set.objects.get(pk=set_id)
				detail = SetDetail()
				detail.set = obj_set
				detail.equipments = set_equipments
				detail.save()				

			return super(EquipmentCreateView, self).form_valid(form)
			
		return super(EquipmentCreateView, self).form_invalid(form)

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
		context = self.get_context_data()
		formset = context['formset']
		if formset.is_valid():
			set_equipments = []
			for form in formset:
				obj = form.save(commit=False)				
				specifications = {}
				type_specifications = form.cleaned_data['model'].type.type_specifications.filter(when='device').exclude(widget='separator')
				for ts in type_specifications:
					key = str(ts.id)
					specifications[key] = form.cleaned_data[key]

				obj.specifications = specifications
				if set_id is not None:					
					obj.in_set = True

				obj.save()
				set_equipments.append(obj.id)			

			return super(EquipmentUpdateView, self).form_valid(form)
			
		return super(EquipmentUpdateView, self).form_invalid(form)

	def get_formset(self):		
		type = self.request.GET.get('type') or self.kwargs.get('type') or None
		set = self.request.GET.get('pk') or self.kwargs.get('pk') or None

		post_data = self.request.POST if self.request.method == 'POST' else None

		if set is not None and type is not None:
			pks = [int(set),]
		elif set is not None:
			set = SetDetail.objects.get(pk=set)
			pks = set.equipments
		
		equipments = Equipment.objects.filter(pk__in=pks)				
		EquipmentFormSet = get_equipment_formset(instances=equipments)							
		formset = EquipmentFormSet(post_data, queryset=equipments)		

		return formset

class SelectTypeListView(ListView):
	model = Type
	template_name = 'stocktaking/select_type.html'

	def get_context_data(self, **kwargs):
		context = super(SelectTypeListView, self).get_context_data()

		if 'model' in self.request.path:
			model = 'model'
		elif 'equipmen' in self.request.path:			
			model = 'equipment'
			sets = Set.objects.all()
			context['sets'] = sets

		context['model'] = model

		return context



















class BrandViewSet(viewsets.ModelViewSet):
	queryset = Brand.objects.all()
	serializer_class = BrandSerializer

class TypeListViewSet(viewsets.ModelViewSet):
	queryset = Type.objects.all()
	serializer_class = TypeListSerializer

	def get_queryset(self):
		queryset = self.queryset
		usage = self.request.query_params.get('usage', None)
		if usage is not None:
			queryset = queryset.filter(usage=usage)
		return queryset

class TypeViewSet(viewsets.ModelViewSet):
	queryset = Type.objects.all()
	serializer_class = TypeSerializer

class ModelListViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Model.objects.all()
	serializer_class = ModelListSerializer

	def get_queryset(self):
		queryset = self.queryset
		type = self.request.query_params.get('type', None)
		if type is not None:
			queryset = queryset.filter(type=type)
		return queryset

class ModelViewSet(viewsets.ModelViewSet):
	queryset = Model.objects.all()
	serializer_class = ModelSerializer

class EquipmentListViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Equipment.objects.all()
	serializer_class = EquipmentListSerializer

	def get_queryset(self):
		queryset = self.queryset
		usage = self.request.query_params.get('usage', None)
		if usage is not None:
			queryset = queryset.filter(model__type__usage=usage)
		return queryset

class EquipmentViewSet(viewsets.ModelViewSet):
	queryset = Equipment.objects.all()
	serializer_class = EquipmentSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
	queryset = Assignment.objects.all()
	serializer_class = AssignmentSerializer

	def get_queryset(self):
		queryset = self.queryset
		equipment = self.request.query_params.get('equipment', None)
		if equipment is not None:
			queryset = queryset.filter(equipment=equipment, is_active=True)
		return queryset