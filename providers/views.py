from django.shortcuts import render
from django.forms.models import modelform_factory
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Provider

class ProviderListView(ListView):
	model = Provider
	template_name = 'providers/providers.html'

	def post(self, request, *args, **kwargs):
		if request.is_ajax():			
			provider_modelform = modelform_factory(Provider, fields=('ruc', 'name', 'representative', 'address', 'city', 'cellphone', 'telephone',))					
    		provider_form = provider_modelform(request.POST)
    		if provider_form.is_valid():
    			object = provider_form.save()
    			data = model_to_dict(object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)				

class ProviderDetailView(DetailView):
	model = Provider

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)		    
		    return JsonResponse(data)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():				
			self.object = self.get_object()
			provider_modelform = modelform_factory(Provider, fields=('ruc', 'name', 'representative', 'address', 'city', 'cellphone', 'telephone',))					
    		provider_form = provider_modelform(request.POST, instance=self.object)
    		if provider_form.is_valid():
    			provider_form.save()
    			data = model_to_dict(self.object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)						

	def delete(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			self.object.delete()
			return JsonResponse({})

