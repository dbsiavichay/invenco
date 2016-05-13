from django.shortcuts import render
from django.forms.models import modelform_factory
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Provider
from equipment.mixins import ListViewMixin, DetailViewMixin

class ProviderListView(ListViewMixin, ListView):
	model = Provider
	template_name = 'providers/providers.html'
	paginate_by = 10

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			filter_fields = ('ruc', 'name', 'address')
			data = self.get_filter_objects(filter_fields)
			data['object_list'] = [model_to_dict(obj) for obj in data['object_list']]
			return JsonResponse(data, safe=False)
		else:
			return super(ProviderListView, self).get(self, request, *args, **kwargs)

class ProviderDetailView(DetailView):
	model = Provider

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)
		    return JsonResponse(data)
