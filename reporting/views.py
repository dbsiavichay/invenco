from django.http import HttpResponse
from django.shortcuts import render
from pdfreports import *

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
