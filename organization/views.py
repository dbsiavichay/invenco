from django.shortcuts import render
from django.forms.models import modelform_factory
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Section, Employee


class SectionListView(ListView):
	model = Section

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			department = request.GET.get('department', None)
			objects = self.model.objects.using('sim').all()
			if (department is not None):
				objects = objects.filter(department=department)
			list = [model_to_dict(object) for object in objects]
			return JsonResponse(list, safe=False)
		else:
			return JsonResponse({}, status=400)

class EmployeeListView(ListView):
	model = Employee

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
			department = request.GET.get('department', None)
			area = request.GET.get('area', None);
			objects = Employee.objects.using('sim').filter(contributor__state='ACTIVO')
			if (department is not None and area is not None):
				objects = objects.filter(department=department, section=area)
			list = []
			for object in objects:
				#dict = model_to_dict(object)
				dict = {}
				dict['charter'] = object.contributor.charter
 				dict['fullname'] = object.contributor.name
				list.append(dict)
			return JsonResponse(list, safe=False)
		else:
			return JsonResponse({}, status=400);
