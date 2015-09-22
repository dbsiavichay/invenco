from django.shortcuts import render, render_to_response
from django.http import HttpResponse

def jobs(request):
	return render_to_response('structure/areas.html', {})
