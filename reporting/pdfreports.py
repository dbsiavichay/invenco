# -*- coding: utf-8 -*-
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table, Image
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.units import cm, mm
from io import BytesIO
from PIL import Image as PilImage

from services import *
from stocktaking.models import Type, Equipment




PDF_TITLE = 'GOBIERNO MUNICIPAL DEL CANTÓN MORONA'

def pdf_equipments():
	types = Type.objects.all()

	#Document settings
	buff = BytesIO()
	doc = SimpleDocTemplate(buff, pagesize=landscape(A4), rightMargin=60, leftMargin=40, topMargin=75, bottomMargin=50,)

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