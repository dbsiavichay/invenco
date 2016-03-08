import json
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from django.forms.models import modelform_factory
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from organization.models import Department, Employee
from equipment.models import Type
from .models import Allocation

class AllocationListView(ListView):
	model = Allocation
	template_name = 'allocation/allocations.html'
	queryset = model.objects.filter(is_active=True)
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(AllocationListView, self).get_context_data(**kwargs)
		types = Type.objects.all()
		departments = Department.objects.using('sim').all()
		#employees = Employee.objects.using('sim').filter(contributor__state='ACTIVO')

		context['types'] = types
		context['departments'] = departments
		#context['employees'] = employees
		return context

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			employee = request.GET.get('employee', None)
			keyword = request.GET.get('keyword', None)
			num_page = request.GET.get('page', None)
			if employee is not None:
				objects = self.model.objects.filter(employee=employee, is_active=True)
				list = []
				for object in objects:
					dict = model_to_dict(object)
					dict['code'] = object.device.code
					dict['name'] = '%s %s %s' % (object.device.model.type, object.device.model.trademark, object.device.model)
					list.append(dict)
				return JsonResponse(list, safe=False)
			elif keyword is not None:
				list = self.queryset.filter(Q(device__model__name__icontains=keyword) |
					Q(device__model__specifications__icontains=keyword) | Q(device__model__type__name__icontains=keyword) |
					Q(device__model__trademark__name__icontains=keyword) | Q(device__code__icontains=keyword))
				paginator = Paginator(list, self.paginate_by)
				page = paginator.page(num_page) if num_page is not None else paginator.page(1)
				object_list = page.object_list
				data = [{'id':object.id, 'model': str(object.device.model), 'code': object.device.code,
					'state': object.device.get_state_icon(),
					'location': object.location(), 'reponsible': object.responsible()} for object in object_list]
				data.append({
					'has_next': page.has_next(),
					'next_page_number': page.next_page_number() if page.has_next() else -1
				})
				return JsonResponse(data, safe=False)
			return JsonResponse({}, status=400)
		else:
			return super(AllocationListView, self).get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			allocation_modelform = modelform_factory(Allocation, fields=('employee','department','area','date_joined','is_active','device',))
    		allocation_form = allocation_modelform(request.POST)
    		if allocation_form.is_valid():
    			object = allocation_form.save()
    			dict = json.loads(request.POST['specifications'])
    			object.device.specifications.update(dict)
    			object.device.save()
    			data = model_to_dict(object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)

class AllocationDetailView(DetailView):
	model = Allocation

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)
		    return JsonResponse(data)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			allocation_modelform = modelform_factory(Allocation, fields=('employee','department','area','date_joined','is_active','device',))
    		allocation_form = allocation_modelform(request.POST)
    		if allocation_form.is_valid():
    			self.object.is_active = False
    			self.object.save()
    			allocation_form.save()
    			data = model_to_dict(self.object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)

	def delete(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			self.object.delete()
			return JsonResponse({})
