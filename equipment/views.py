from django.shortcuts import render
from django.forms.models import modelform_factory
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Trademark, Type, Model

class TrademarkListView(ListView):
	model = Trademark
	template_name = 'equipment/trademarks.html'

	def post(self, request, *args, **kwargs):
		if request.is_ajax():			
			trademark_modelform = modelform_factory(Trademark, fields=('name',))					
    		trademark_form = trademark_modelform(request.POST)
    		if trademark_form.is_valid():
    			object = trademark_form.save()
    			data = model_to_dict(object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)				

class TrademarkDetailView(DetailView):
	model = Trademark

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)		    
		    return JsonResponse(data)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():				
			self.object = self.get_object()
			trademark_modelform = modelform_factory(Trademark, fields=('name',))					
    		trademark_form = trademark_modelform(request.POST, instance=self.object)
    		if trademark_form.is_valid():
    			trademark_form.save()
    			data = model_to_dict(self.object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)						

	def delete(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			self.object.delete()
			return JsonResponse({})

class TypeListView(ListView):
	model = Type
	template_name = 'equipment/types.html'

	def post(self, request, *args, **kwargs):
		if request.is_ajax():				
			type_modelform = modelform_factory(Type, fields=('name', 'specifications'))					
    		type_form = type_modelform(request.POST)     		
    		if type_form.is_valid():    			    			
    			object = type_form.save()
    			data = model_to_dict(object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)				

class TypeDetailView(DetailView):
	model = Type

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)		    
		    return JsonResponse(data)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():				
			self.object = self.get_object()
			type_modelform = modelform_factory(Type, fields=('name', 'specifications'))					
    		type_form = type_modelform(request.POST, instance=self.object)
    		if type_form.is_valid():
    			type_form.save()
    			data = model_to_dict(self.object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)						

	def delete(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			self.object.delete()
			return JsonResponse({})

class ModelListView(ListView):
	model = Model
	template_name = 'equipment/models.html'

	def get_context_data(self, **kwargs):
		context = super(ModelListView, self).get_context_data(**kwargs)
		types = Type.objects.all()
		trademarks = Trademark.objects.all()

		context['types'] = types
		context['trademarks'] = trademarks
		return context

	def post(self, request, *args, **kwargs):
		if request.is_ajax():				
			model_modelform = modelform_factory(Model, fields=('name', 'specifications'))					
    		model_form = model_modelform(request.POST)     		
    		if model_form.is_valid():    			    			
    			object = model_form.save()
    			data = model_to_dict(object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)				

class ModelDetailView(DetailView):
	model = Model

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)		    
		    return JsonResponse(data)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():				
			self.object = self.get_object()
			model_modelform = modelform_factory(Model, fields=('name', 'specifications'))					
    		model_form = model_modelform(request.POST, instance=self.object)
    		if model_form.is_valid():
    			model_form.save()
    			data = model_to_dict(self.object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)						

	def delete(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			self.object.delete()
			return JsonResponse({})

