from django.shortcuts import render
from rest_framework import viewsets
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from pure_pagination.mixins import PaginationMixin
from .models import *
from .serializers import *

class BuildingListView(PaginationMixin, ListView):
	model = Building
	paginate_by = 8

class BuildingCreateView(CreateView):
	model = Building
	fields = '__all__'
	success_url = '/building/'

class BuildingUpdateView(UpdateView):
	model = Building
	fields = '__all__'
	success_url = '/building/'

class BuildingDeleteView(DeleteView):
	model = Building
	success_url = '/building/'


class DepartmentViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Department.objects.using('sim').all()
	serializer_class = DepartmentSerializer

class SectionViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Section.objects.using('sim').all()
	serializer_class = SectionSerializer

	def get_queryset(self):
		queryset = self.queryset
		department = self.request.query_params.get('department', None)
		if department is not None:
			queryset = queryset.filter(department=department)
		return queryset

class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
	queryset = Employee.objects.using('sim').filter(contributor__state='ACTIVO')
	serializer_class = EmployeeSerializer
