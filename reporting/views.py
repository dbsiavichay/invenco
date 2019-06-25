from django.http import HttpResponse
from django.shortcuts import render
from pdfreports import *

from django.views.generic import DetailView
from stocktaking.models import Dispatch

def equipment_report(response):

    # Create the HttpResponse object with the appropriate PDF headers.
	response = HttpResponse(content_type='application/pdf')
	# Para visualizar en el navegador
	#response['Content-Disposition'] = 'inline; filename=report.pdf'
	# Para descargar
	response['Content-Disposition'] = 'attachment; filename="report.pdf"' 

	pdf = pdf_equipments()

    # Get the value of the StringIO buffer and write it to the response.
	response.write(pdf)
	return response

class DispatchPrintView(DetailView):
	model = Dispatch

	def get(self, request, *args, **kwargs):
		response = HttpResponse(content_type='application/pdf')		
		response['Content-Disposition'] = 'attachment; filename="report.pdf"' 
		pdf = get_pdf_dispatch(self.get_object())	 
		response.write(pdf)
		return response