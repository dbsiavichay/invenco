from django.shortcuts import render
from django.forms.models import modelform_factory
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from equipment.models import Type
from organization.models import Department
from .models import Allocation

class AllocationListView(ListView):
	model = Allocation
	template_name = 'allocation/allocations.html'

	def get_context_data(self, **kwargs):
		context = super(AllocationListView, self).get_context_data(**kwargs)		
		types = Type.objects.all()
		departments = Department.objects.all()	

		context['object_list'] = context['object_list'].filter(is_active=True)
		context['types'] = types
		context['departments'] = departments
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
			allocation_modelform = modelform_factory(Allocation, fields=('date_joined', 'is_active', 'employee', 'device'))					
    		allocation_form = allocation_modelform(request.POST)
    		if allocation_form.is_valid():
    			object = allocation_form.save()
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
			allocation_modelform = modelform_factory(Allocation, fields=('date_joined', 'is_active', 'employee', 'device'))					
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
