from django.shortcuts import render
from django.shortcuts import render
from django.forms.models import modelform_factory
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from allocation.models import Allocation
from equipment.models import Device, Type
from .models import Maintenance, Parts

class MaintenanceListView(ListView):
	model = Maintenance
	template_name = 'technical_assistance/maintenances.html'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(MaintenanceListView, self).get_context_data(**kwargs)

		allocations = Allocation.objects.filter(is_active=True)
		devices = Device.objects.filter(model__type__is_part=True).exclude(parts__pk__gt=0)

		context['allocations'] = allocations
		context['devices'] = devices
		return context

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			specifications = request.POST.get('specifications', None)
			maintenance_modelform = modelform_factory(Maintenance, fields=('date', 'problem', 'solution', 'device', ))
    		maintenance_form = maintenance_modelform(request.POST)
    		if maintenance_form.is_valid() and specifications is not None:
				object = maintenance_form.save()
				object.device.specifications = specifications
				object.device.save()
				data = model_to_dict(object)
				parts = request.POST['parts'].split(',') if request.POST['parts'] != '' else []
				for id in parts:
					device = Device.objects.get(pk=id)
					part = Parts(is_active=True, part=device, maintenance=object)
					part.save()
				return JsonResponse(data)
    		return JsonResponse({}, status=400)

class MaintenanceDetailView(DetailView):
	model = Maintenance

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)
		    parts = []
		    for part in Parts.objects.filter(maintenance = self.object):
		    	item = model_to_dict(part)
		    	item['name'] = str(part)
		    	parts.append(item)
		    data['parts'] = parts
		    return JsonResponse(data, safe=False)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			specifications = request.POST.get('specifications', None)
			self.object = self.get_object()
			maintenance_modelform = modelform_factory(Maintenance, fields=('date', 'problem', 'solution', 'device', ))
			maintenance_form = maintenance_modelform(request.POST, instance=self.object)
			if maintenance_form.is_valid() and specifications is not None:
				maintenance_form.save()
				self.object.device.specifications = specifications
				self.object.device.save()
				self.object.parts_set.all().delete()
				data = model_to_dict(self.object)
				parts = request.POST['parts'].split(',') if request.POST['parts'] != '' else []
				for id in parts:
					device = Device.objects.get(pk=id)
					part = Parts(is_active=True, part=device, maintenance=self.object)
					part.save()
				return JsonResponse(data)
			return JsonResponse({}, status=400)

	def delete(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			self.object.delete()
			return JsonResponse({})
