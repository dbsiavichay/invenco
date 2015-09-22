from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
from .models import Job

def jobs(request):

	jobs = Job.objects.all()

	return render_to_response('structure/jobs.html', {'jobs': jobs})

def job(request, job_id):

	job = Job.objects.get(pk=job_id)
	response = JsonResponse({'id': job.id, 'name': job.name})
	return HttpResponse(response)

