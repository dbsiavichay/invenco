from django.shortcuts import render
from django.forms.models import modelform_factory
from django.forms import model_to_dict
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from .models import Job, Department, Area, Employee

class JobListView(ListView):
	model = Job
	template_name = 'structure/jobs.html'

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


class AreaListView(ListView):
	model = Area
	template_name = 'structure/areas.html'

	def get_context_data(self, **kwargs):
		context = super(AreaListView, self).get_context_data(**kwargs)

		departments = Department.objects.all()
		context['departments'] = departments

		return context

	def get(self, request, *args, **kwargs):		
		if request.is_ajax():
			department = request.GET.get('department', None);
			if (department is not None):				
				objects = self.model.objects.filter(department=department)				
				list = [model_to_dict(object) for object in objects]
				return JsonResponse(list, safe=False)
			return JsonResponse({}, status=400);
		else:
			return super(AreaListView, self).get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():			
			area_modelform = modelform_factory(Area, fields=('code', 'name', 'department'))					
    		area_form = area_modelform(request.POST)
    		if area_form.is_valid():
    			object = area_form.save()
    			data = model_to_dict(object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)				

class AreaDetailView(DetailView):
	model = Area

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    data = model_to_dict(self.object)		    
		    return JsonResponse(data)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():				
			self.object = self.get_object()
			area_modelform = modelform_factory(Area, fields=('code', 'name', 'department'))					
    		area_form = area_modelform(request.POST, instance=self.object)
    		if area_form.is_valid():
    			area_form.save()
    			data = model_to_dict(self.object)
    			return JsonResponse(data)
    		return JsonResponse({}, status=400)						

	def delete(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			self.object.delete()
			return JsonResponse({})

class EmployeeListView(ListView):
	model = Employee
	template_name = 'structure/employees.html'

	def get_context_data(self, **kwargs):
		context = super(EmployeeListView, self).get_context_data(**kwargs)

		departments = Department.objects.all()
		jobs = Job.objects.all()
		context['departments'] = departments
		context['jobs'] = jobs

		return context

	def get(self, request, *args, **kwargs):		
		if request.is_ajax():
			area = request.GET.get('area', None);
			if (area is not None):				
				objects = self.model.objects.filter(area=area)				
				list = []
				for object in objects:
					dict = model_to_dict(object)
					dict['full_name'] = '%s %s' % (object.user.first_name, object.user.last_name)
					list.append(dict)
				return JsonResponse(list, safe=False)
			return JsonResponse({}, status=400);
		else:
			return super(EmployeeListView, self).get(self, request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():
			user_modelform = modelform_factory(User, fields=('first_name', 'last_name', 'email', 'username', 'password', 'is_active', 'date_joined'))
			user_form = user_modelform(request.POST)
			if user_form.is_valid():
				user = user_form.save()
				dict = request.POST.copy()
				dict['user'] = user.id			
				employee_modelform = modelform_factory(Employee, fields=('charter', 'extension', 'is_head', 'area', 'job', 'user'))					
	    		employee_form = employee_modelform(dict)
	    		if employee_form.is_valid():
	    			object = employee_form.save()
	    			data = model_to_dict(object)
	    			return JsonResponse(data)
	    		user.delete()
	    		return JsonResponse({}, status=400)
	    	return JsonResponse({}, status=400)			

class EmployeeDetailView(DetailView):
	model = Employee

	def get(self, request, *args, **kwargs):
		if request.is_ajax():
		    self.object = self.get_object()
		    user_dict = model_to_dict(self.object.user)
		    data = model_to_dict(self.object)
		    data.update(user_dict)
		    data.update({'department': self.object.area.department.id})		    
		    return JsonResponse(data)

	def post(self, request, *args, **kwargs):
		if request.is_ajax():				
			self.object = self.get_object()
			user_modelform = modelform_factory(User, fields=('first_name', 'last_name', 'email', 'username', 'password', 'is_active', 'date_joined'))
			user_form = user_modelform(request.POST, instance=self.object.user)
			if user_form.is_valid():
				user = user_form.save()
				dict = request.POST.copy()
				dict['user'] = user.id	
				employee_modelform = modelform_factory(Employee, fields=('charter', 'extension', 'is_head', 'area', 'job', 'user'))					
	    		employee_form = employee_modelform(dict, instance=self.object)
	    		if employee_form.is_valid():
	    			employee_form.save()
	    			data = model_to_dict(self.object)
	    			return JsonResponse(data)
	    		return JsonResponse({}, status=400)
	    	return JsonResponse({}, status=400)						

	def delete(self, request, *args, **kwargs):
		if request.is_ajax():
			self.object = self.get_object()
			self.object.user.delete()
			return JsonResponse({})