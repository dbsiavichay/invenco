from rest_framework import viewsets
from .models import *

from .serializers import *

class BrandViewSet(viewsets.ModelViewSet):
	queryset = Brand.objects.all()
	serializer_class = BrandSerializer

class TypeListViewSet(viewsets.ModelViewSet):
	queryset = Type.objects.all()
	serializer_class = TypeListSerializer

	def get_queryset(self):
		queryset = self.queryset
		usage = self.request.query_params.get('usage', None)
		if usage is not None:
			queryset = queryset.filter(usage=usage)
		return queryset

class TypeViewSet(viewsets.ModelViewSet):
	queryset = Type.objects.all()
	serializer_class = TypeSerializer

class ModelListViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Model.objects.all()
	serializer_class = ModelListSerializer

	def get_queryset(self):
		queryset = self.queryset
		type = self.request.query_params.get('type', None)
		if type is not None:
			queryset = queryset.filter(type=type)
		return queryset

class ModelViewSet(viewsets.ModelViewSet):
	queryset = Model.objects.all()
	serializer_class = ModelSerializer

class EquipmentListViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Equipment.objects.all()
	serializer_class = EquipmentListSerializer

	def get_queryset(self):
		queryset = self.queryset
		usage = self.request.query_params.get('usage', None)
		if usage is not None:
			queryset = queryset.filter(model__type__usage=usage)
		return queryset

class EquipmentViewSet(viewsets.ModelViewSet):
	queryset = Equipment.objects.all()
	serializer_class = EquipmentSerializer

class AssignmentViewSet(viewsets.ModelViewSet):
	queryset = Assignment.objects.all()
	serializer_class = AssignmentSerializer

	def get_queryset(self):
		queryset = self.queryset
		equipment = self.request.query_params.get('equipment', None)
		if equipment is not None:
			queryset = queryset.filter(equipment=equipment, is_active=True)
		return queryset