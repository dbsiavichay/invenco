import json
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
			if (employee is not None):
				objects = self.model.objects.filter(employee=employee, is_active=True)
				list = []
				for object in objects:
					dict = model_to_dict(object)
					dict['code'] = object.device.code
					dict['name'] = '%s %s %s' % (object.device.model.type, object.device.model.trademark, object.device.model)
					list.append(dict)
				return JsonResponse(list, safe=False)
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
