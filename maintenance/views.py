from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from django.forms import modelformset_factory, formset_factory

from .models import *
#from .forms import *
#from .mixins import *

from pure_pagination.mixins import PaginationMixin


class FixListView(PaginationMixin, ListView):
	model = Fix
	paginate_by = 8

class FixCreateView(CreateView):
	model = Fix
	fields = '__all__'
	success_url = '/fix/'