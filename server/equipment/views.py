from django.db.models import Q
from django.forms import model_to_dict
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView
from allocation.models import Allocation
from organization.models import Contributor
from purchases.models import Provider
from .models import Trademark, Type, Model, Device
from .mixins import ListViewMixin, DetailViewMixin
from .reports import get_pdf, get_pcdir
from rest_framework import viewsets

from .serializers import *

class TrademarkViewSet(viewsets.ModelViewSet):
	queryset = Trademark.objects.all()
	serializer_class = TrademarkSerializer

class TypeListViewSet(viewsets.ModelViewSet):
	queryset = Type.objects.all()
	serializer_class = TypeListSerializer

class TypeViewSet(viewsets.ModelViewSet):
	queryset = Type.objects.all()
	serializer_class = TypeSerializer

class ModelListViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Model.objects.all()
	serializer_class = ModelListSerializer

class ModelViewSet(viewsets.ModelViewSet):
	queryset = Model.objects.all()
	serializer_class = ModelSerializer

	def get_queryset(self):
		queryset = self.queryset
		type = self.request.query_params.get('type', None)
		if type is not None:
			queryset = queryset.filter(type=type)
		return queryset

class DeviceListViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Device.objects.all()
	serializer_class = DeviceListSerializer

class DeviceViewSet(viewsets.ModelViewSet):
	queryset = Device.objects.all()
	serializer_class = DeviceSerializer

class TrademarkListView(ListViewMixin, ListView):
	model = Trademark
	template_name = 'equipment/trademarks.html'
	paginate_by = 10

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			filter_fields = ('name',)
			data = self.get_filter_objects(filter_fields)
			data['object_list'] = [model_to_dict(obj) for obj in data['object_list']]
			return JsonResponse(data, safe=False)
		else:
			return super(TrademarkListView, self).get(self, request, *args, **kwargs)

class TrademarkDetailView(DetailViewMixin, DetailView):
	model = Trademark

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)
		    return JsonResponse(data)

class TypeListView(ListViewMixin, ListView):
	model = Type
	template_name = 'equipment/types.html'
	paginate_by = 10

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			filter_fields = ('name',)
			data = self.get_filter_objects(filter_fields)
			data['object_list'] = [{'id':obj.id, 'name': obj.name, 'specifications': str(obj.specifications)} for obj in data['object_list']]
			return JsonResponse(data, safe=False)
		else:
			return super(TypeListView, self).get(self, request, *args, **kwargs)

class TypeDetailView(DetailViewMixin, DetailView):
	model = Type

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)
		    return JsonResponse(data)

class ModelListView(ListViewMixin, ListView):
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
			str_type = request.GET.get('type', None)
			if str_type is not None:
				objects = self.model.objects.filter(type=str_type)
				object_list = []
				for obj in objects:
					obj_dict = model_to_dict(obj)
					obj_dict['trademark'] = obj.trademark.name
					object_list.append(obj_dict)
				return JsonResponse(object_list, safe=False)
			else:
				filter_fields = ('name', 'type__name', 'trademark__name')
				data = self.get_filter_objects(filter_fields)
				data['object_list'] = [{'id': obj.id,  'name':obj.name, 'type': obj.type.name, 'trademark': obj.trademark.name,} for obj in data['object_list']]
				return JsonResponse(data, safe=False)

			return JsonResponse({}, status=400)
		else:
			return super(ModelListView, self).get(self, request, *args, **kwargs)

class ModelDetailView(DetailViewMixin, DetailView):
	model = Model

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)
		    return JsonResponse(data)

class DeviceListView(ListViewMixin, ListView):
	model = Device
	template_name = 'equipment/devices.html'
	paginate_by = 20

	def get_context_data(self, **kwargs):
		context = super(DeviceListView, self).get_context_data(**kwargs)
		types = Type.objects.all()
		providers = Provider.objects.all()

		context['types'] = types
		context['providers'] = providers

		return context

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			str_type = request.GET.get('type', None)
			if str_type is not None:
				objects = self.model.objects.filter(model__type=str_type)
				object_list = []
				for obj in objects:
					allocations = Allocation.objects.filter(device=obj, is_active=True)
					is_assigned = len(allocations) > 0
					obj_dict = model_to_dict(obj)
					obj_dict['type'] = obj.model.type.name
					obj_dict['trademark'] = obj.model.trademark.name
					obj_dict['model'] = obj.model.name
					obj_dict['is_assigned'] = is_assigned
					if is_assigned:
						obj_dict['subtext'] = allocations[0].short_responsible()

					object_list.append(obj_dict)
				return JsonResponse(object_list, safe=False)
			else:
				filter_fields = ('model__name', 'model__specifications', 'model__type__name', 'model__trademark__name', 'code', 'provider__name', 'invoice')
				data = self.get_filter_objects(filter_fields)
				data['object_list'] = [{'id':obj.id, 'model': str(obj.model.type) + ' ' + str(obj.model), 'code': obj.code,
					'provider': '%s | %s' % (str(obj.provider), obj.invoice) if obj.provider else '', 'state': obj.get_state_icon(),
					'date_warranty': obj.get_timeuntil()} for obj in data['object_list']]
				return JsonResponse(data, safe=False)
			return JsonResponse({}, status=400);
		else:
			return super(DeviceListView, self).get(self, request, *args, **kwargs)

class DeviceDetailView(DetailViewMixin, DetailView):
	model = Device

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			data = model_to_dict(self.object)
			data['type'] = self.object.model.type.id
			data['type_name'] = str(self.object.model.type)
			data['model_name'] = str(self.object.model)
			data['model_specifications'] = self.object.model.specifications

			return JsonResponse(data)

class ReportListView(ListView):
	model = Type
	template_name = 'equipment/reports.html'
	queryset = model.objects.filter(usage=1)

	def get(self, request, *args, **kwargs):
		stroptions = request.GET.get('options', None)
		t = request.GET.get('type', None)
		if stroptions is not None:
			options = [int(opt) for opt in stroptions.split(',')]
			pdf = get_pdf(options)
			response = HttpResponse(content_type='application/pdf')
			response.write(pdf)
			return response
		elif t is not None:
			pdf = get_pcdir()
			response = HttpResponse(content_type='application/pdf')
			response.write(pdf)
			return response
		else:
			return super(ReportListView, self).get(self, request, *args, **kwargs)
