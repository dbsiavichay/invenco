from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import render
from django.forms.models import modelform_factory
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView
from allocation.models import Allocation
from organization.models import Contributor
from providers.models import Provider
from .models import Trademark, Type, Model, Device
from .reports import get_pdf

class TrademarkListView(ListView):
	model = Trademark
	template_name = 'equipment/trademarks.html'
	paginate_by = 10

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			keyword = request.GET.get('keyword', None)
			num_page = request.GET.get('page', None)
			list = self.model.objects.filter(name__icontains=keyword)
			paginator = Paginator(list, self.paginate_by)
			page = paginator.page(num_page) if num_page is not None else paginator.page(1)
			object_list = page.object_list
			data = [model_to_dict(object) for object in object_list]
			data.append({
				'has_next': page.has_next(),
				'next_page_number': page.next_page_number() if page.has_next() else -1
			})
			return JsonResponse(data, safe=False)
		else:
			return super(TrademarkListView, self).get(self, request, *args, **kwargs)

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
	paginate_by = 10

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			type_modelform = modelform_factory(Type, fields=('name', 'is_part', 'specifications'))
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
			type_modelform = modelform_factory(Type, fields=('name', 'is_part', 'specifications'))
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
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(ModelListView, self).get_context_data(**kwargs)
		types = Type.objects.all()
		trademarks = Trademark.objects.all()

		context['types'] = types
		context['trademarks'] = trademarks
		return context

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			type = request.GET.get('type', None)
			keyword = request.GET.get('keyword', None)
			num_page = request.GET.get('page', None)
			if type is not None:
				objects = self.model.objects.filter(type=type)
				list = []
				for object in objects:
					dict = model_to_dict(object)
					dict['trademark'] = object.trademark.name
					list.append(dict)
				return JsonResponse(list, safe=False)
			elif keyword is not None:
				objects = self.model.objects.filter(Q(name__icontains=keyword)|Q(type__name__icontains=keyword)|Q(trademark__name__icontains=keyword))
				paginator = Paginator(objects, self.paginate_by)
				page = paginator.page(num_page) if num_page is not None else paginator.page(1)
				object_list = page.object_list
				data = [{'id': object.id,  'name':object.name, 'type': object.type.name, 'trademark': object.trademark.name,} for object in object_list]
				data.append({
					'has_next': page.has_next(),
					'next_page_number': page.next_page_number() if page.has_next() else -1
				})
				return JsonResponse(data, safe=False)

			return JsonResponse({}, status=400)
		else:
			return super(ModelListView, self).get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			model_modelform = modelform_factory(Model, fields=('name', 'specifications', 'type', 'trademark'))
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
			model_modelform = modelform_factory(Model, fields=('name', 'specifications', 'type', 'trademark'))
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

class DeviceListView(ListView):
	model = Device
	template_name = 'equipment/devices.html'
	paginate_by = 10

	def get_context_data(self, **kwargs):
		context = super(DeviceListView, self).get_context_data(**kwargs)
		types = Type.objects.all()
		providers = Provider.objects.all()

		context['types'] = types
		context['providers'] = providers

		return context

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			type = request.GET.get('type', None);
			if (type is not None):
				objects = self.model.objects.filter(model__type=type)
				list = []
				for object in objects:
					allocations = Allocation.objects.filter(device=object, is_active=True)
					is_assigned = len(allocations) > 0
					dict = model_to_dict(object)
					dict['type'] = object.model.type.name
					dict['trademark'] = object.model.trademark.name
					dict['model'] = object.model.name
					dict['is_assigned'] = is_assigned
					if is_assigned:
						dict['subtext'] = allocations[0].short_responsible()

					list.append(dict)
				return JsonResponse(list, safe=False)
			return JsonResponse({}, status=400);
		else:
			return super(DeviceListView, self).get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			model_modelform = modelform_factory(Device, fields=('code', 'serial', 'part', 'state', 'invoice', 'date_purchase', 'date_warranty', 'specifications', 'model', 'provider',))
    		model_form = model_modelform(request.POST)
    		if model_form.is_valid():
    			object = model_form.save()
    			data = model_to_dict(object)
    			return JsonResponse(data)
    		print model_form.errors
    		return JsonResponse({}, status=400)

class DeviceDetailView(DetailView):
	model = Device

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)
		    data['type'] = self.object.model.type.id
		    return JsonResponse(data)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			model_modelform = modelform_factory(Device, fields=('code', 'serial', 'part', 'state', 'invoice', 'date_purchase', 'date_warranty', 'specifications', 'model', 'provider',))
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

class ReportListView(ListView):
	model = Type
	template_name = 'equipment/reports.html'
	queryset = model.objects.filter(is_part=False)

	def get(self, request, *args, **kwargs):
		stroptions = request.GET.get('options', None);
		if stroptions is not None:
			options = stroptions.split(',')
			pdf = get_pdf(options)
			response = HttpResponse(content_type='application/pdf')
			response.write(pdf)
			return response
		else:
			return super(ReportListView, self).get(self, request, *args, **kwargs)
