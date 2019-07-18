# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, Image, Spacer
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.lib.units import cm, mm
from io import BytesIO
from PIL import Image as PilImage

from services import *
from stocktaking.models import Type, Equipment

from datetime import datetime


PDF_TITLE = 'GOBIERNO MUNICIPAL DEL CANTÓN MORONA'

def pdf_equipments():
	types = Type.objects.all()

	#Document settings
	buff = BytesIO()
	doc = SimpleDocTemplate(buff, pagesize=A4, rightMargin=60, leftMargin=40, topMargin=75, bottomMargin=50,)

	#Styles settings
	styles = getSampleStyleSheet()
	report = [
		Paragraph(PDF_TITLE, styles['Title']),
	]

	for type in types:
		table = get_table_equipments(type)
		if table is not None:
			report+=table

	doc.build(report, onFirstPage=get_letterhead_page,onLaterPages=get_letterhead_page)
	return buff.getvalue()

def get_pdf_dispatch(obj):
	buff = BytesIO()
	doc = SimpleDocTemplate(buff, pagesize=A4, rightMargin=60, leftMargin=40, topMargin=75, bottomMargin=50,)

	story = [get_title_paragraph('ORDEN DE DESPACHO PARA BIENES DE BODEGA')]
	story.append(get_title_paragraph('N° GMCM-DGA-%s-%s' % (obj.id, obj.date.year), 12))
	story.append(Spacer(0, 0.5*cm))
	date = get_paragraph('Macas, ' + datetime.now().strftime("%d/%m/%Y"))
	date.style.alignment = TA_RIGHT
	story.append(date)
	story.append(Spacer(A4[0], 1*cm))
	story.append(get_paragraph('Ing. Cristian Navarro'))
	story.append(get_strong_text('ESPECIALISTA DE CONTROL Y SUPERVISIÓN DE BIENES PÚBLICOS', 12))
	story.append(Spacer(A4[0], 1*cm))
	request = 'Solicito a usted se sirva realizar el despacho correspondiente de los siguiente bienes al Sr/a {}, funcionario del Gobierno Municipal del Cantón Morona.'
	request = get_paragraph(request.format(obj.get_employee()))
	request.style.alignment = TA_JUSTIFY
	story.append(request)
	story = story + get_table_dispatch(obj)
	story.append(get_strong_text('Observaciones:', 12))	
	if obj.observation: story.append(get_paragraph(obj.observation))
	director = ('Ing. Patricia Cabrera', 'DIRECTOR DE GESTIÓN ADMINISTRATIVA')
	solicitante = ('Sr/a. ' + obj.get_employee(), 'FUNCIONARIO')
	story = story + get_signatures([director, solicitante])	
	doc.build(story, onFirstPage=get_letterhead_page,onLaterPages=get_letterhead_page)
	return buff.getvalue()
