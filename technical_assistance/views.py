from django.shortcuts import render
from django.shortcuts import render
from django.forms.models import modelform_factory
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from allocation.models import Allocation
from .models import Maintenance, Parts


class MaintenanceListView(ListView):
	model = Maintenance
	template_name = 'technical_assistance/maintenances.html'

	def get_context_data(self, **kwargs):
		context = super(MaintenanceListView, self).get_context_data(**kwargs)

		allocations = Allocation.objects.filter(is_active=True)

		context['allocations'] = allocations
		return context

	def post(self, request, *args, **kwargs):
		if request.is_ajax():			
			maintenance_modelform = modelform_factory(Maintenance, fields=('name',))					
    		maintenance_form = maintenance_modelform(request.POST)
    		if maintenance_form.is_valid():
    			object = maintenance_form.save()
    			data = model_to_dict(object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)				

class MaintenanceDetailView(DetailView):
	model = Maintenance

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)		    
		    return JsonResponse(data)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():				
			self.object = self.get_object()
			maintenance_modelform = modelform_factory(Maintenance, fields=('name',))					
    		maintenance_form = maintenance_modelform(request.POST, instance=self.object)
    		if maintenance_form.is_valid():
    			maintenance_form.save()
    			data = model_to_dict(self.object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)						

	def delete(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			self.object.delete()
			return JsonResponse({})