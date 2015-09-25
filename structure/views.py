from django.shortcuts import render, redirect
from django.forms.models import modelform_factory
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from .models import Job, Department

class JobListView(ListView):
	model = Job
	template_name = 'structure/jobs.html'

	def get_context_data(self, **kwargs):
		context = super(JobListView, self).get_context_data(**kwargs)
		context['modal_title'] = 'Datos de Cargo'
		return context

	def post(self, request, *args, **kwargs):
		if request.is_ajax():			
			job_modelform = modelform_factory(Job, fields=('name',))					
    		job_form = job_modelform(request.POST)
    		if job_form.is_valid():
    			object = job_form.save()
    			data = model_to_dict(object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)				

class JobDetailView(DetailView):
	model = Job

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)		    
		    return JsonResponse(data)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():				
			self.object = self.get_object()
			job_modelform = modelform_factory(Job, fields=('name',))					
    		job_form = job_modelform(request.POST, instance=self.object)
    		if job_form.is_valid():
    			job_form.save()
    			data = model_to_dict(self.object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)						

	def delete(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			self.object.delete()
			return JsonResponse({})

class DepartmentListView(ListView):
	model = Department
	template_name = 'structure/departments.html'

	def get_context_data(self, **kwargs):
		context = super(DepartmentListView, self).get_context_data(**kwargs)
		context['modal_title'] = 'Datos de Departamento'
		return context

	def post(self, request, *args, **kwargs):
		if request.is_ajax():			
			department_modelform = modelform_factory(Department, fields=('code', 'name',))					
    		department_form = department_modelform(request.POST)
    		if department_form.is_valid():
    			object = department_form.save()
    			data = model_to_dict(object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)				

class DepartmentDetailView(DetailView):
	model = Department

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)		    
		    return JsonResponse(data)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():				
			self.object = self.get_object()
			department_modelform = modelform_factory(Department, fields=('code', 'name',))					
    		department_form = department_modelform(request.POST, instance=self.object)
    		if department_form.is_valid():
    			department_form.save()
    			data = model_to_dict(self.object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)						

	def delete(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			self.object.delete()
			return JsonResponse({})