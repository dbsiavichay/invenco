from django.shortcuts import render
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