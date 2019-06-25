# -*- coding: utf-8 -*-
from django.conf import settings
from os.path import join

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import Image, Table, TableStyle, Paragraph, Spacer

from stocktaking.models import Equipment

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Helvetica", 10)
        self.drawRightString(115*mm, 5*mm,
            "Página %d de %d" % (self._pageNumber, page_count))

def get_letterhead_page(canvas, doc):
        # Save the state of our canvas so we can draw on it
		canvas.saveState()
		styles = getSampleStyleSheet()
		base_path = join(settings.BASE_DIR, 'static/images/reports/')

		escudo = Image(base_path + 'escudo_morona.png', width=6*cm,height=2*cm)
		#logo = Image(base_path + 'logo_morona.jpg', width=2*cm,height=2*cm)		
		footer_caption = Image(base_path + 'footer-caption.png', width=6.5*cm,height=1.5*cm)
		#footer_image = Image(base_path + 'footer-image.png', width=3*cm,height=1.5*cm)

		w, h = escudo.wrap(doc.width, doc.topMargin)
		escudo.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 20)

		#w, h = logo.wrap(doc.width, doc.topMargin)
		#logo.drawOn(canvas, doc.leftMargin + 700, doc.height + doc.topMargin - 20)
		
		w, h = footer_caption.wrap(doc.width, doc.topMargin)
		footer_caption.drawOn(canvas, doc.leftMargin, doc.height + doc.topMargin - 780)

		#w, h = footer_image.wrap(doc.width, doc.topMargin)
		#footer_image.drawOn(canvas, doc.leftMargin + 700, doc.height + doc.topMargin - 530)

        # Release the canvas
		canvas.restoreState()

### Functions for paragraphs
def get_title_paragraph(text, size=18):
	style = getSampleStyleSheet()['Title']
	style.fontSize = size
	return Paragraph(text, style=style)

def get_strong_text(text, size=10):
	stylesheet=getSampleStyleSheet()
	bold = stylesheet['Heading5']
	bold.fontSize = size
 	return Paragraph(text, style=bold)

def get_paragraph(text, size=12):
	style = getSampleStyleSheet()['Normal']
	style.fontSize = size
	style.leading = size
	return Paragraph(text, style=style)

### Functions for draw tables
def get_table_style(fontSize=6):
	style = TableStyle([
		('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
		('GRID',(0,0),(-1,-1), 0.25, colors.black),
		('VALIGN', (0, 0), (-1, -1), 'TOP'),
		('FONTSIZE', (0, 0), (-1, -1), fontSize),
	])

	return style

def get_list_component(data):
	style = TableStyle([		
		#('GRID',(0,0),(-1,-1), 0.25, colors.black),
		('FONTSIZE', (0, 0), (-1, -1), 6), 
		('LEFTPADDING', (0, 0), (-1, -1), 0), 
		('RIGHTPADDING', (0, 0), (-1, -1), 0), 
		('TOPPADDING', (0, 0), (-1, -1), 0), 
		('BOTTOMPADDING', (0, 0), (-1, -1), 0),
	])

	return Table(data, style=style)


def get_table_title(text):
	styles = getSampleStyleSheet()
	style = styles['Heading5']
	style.fontSize = 12

	title = Paragraph(str(text), style)
	return title

def get_styled_data(data):
	styles = getSampleStyleSheet()

	style = styles['Heading5']
	style.fontSize = 8

	data[0] = (Paragraph(head, style) for head in data[0])
	return data

def get_attribute(instance, field):
	names = field.split('.')
	name = names.pop(0)

	if len(names) == 0:
		if not name:
			return None

		attr = getattr(instance, name)
		
		if callable(attr):
			return  get_paragraph(attr(), 6)
		
		return get_paragraph(str(attr), 6)
 
	return get_attribute(getattr(instance, name), '.'.join(names))

def get_data(object_list, fields ,style=None):
	data = []	
	for obj in object_list:		
		line = [get_attribute(obj, field) for field in fields]
		data.append(line)

	return data


def get_table(queryset, fields, col_widths=None, aling='LEFT'):
	if len(queryset) <= 0:
		return None

	headers = [item.split('as')[1].strip() for item in fields]
	fields = [item.split('as')[0].strip() for item in fields]
	data = get_data(queryset, fields)	
	data = get_styled_data([headers,] + data)
	col_widths = [width*cm for width in col_widths]	
	table = Table(data, cols_widths, style=get_table_style(), hAlign=aling)
	return table

def get_table_equipments(type):
	equipments = Equipment.objects.filter(model__type=type).exclude(state=10)

	if len(equipments) <= 0:
		return None

	table_title = get_table_title(type.name)	
	col_widths = [1.5, 3, 2.3, 1.5, 4, 3]
	fields = ('model.brand as Marca', 'model.name as Equipo', 'serial as Serie', 'code as Código', 'get_responsible as Responsable', 'get_state as Estado')

	# ##Specifications
	#specifications = type.type_specifications.filter(when='device')

	# for i in range(len(equipments)):
	# 	equipment = equipments[i]
	# 	values = []		
		
	# 	for specification in specifications:			
	# 		if specification.widget == 'separator':
	# 			if not specification.label in headers:
	# 				headers.append(specification.label)
	# 			if len(values) > 0:
	# 				data[i].append(get_list_component(values))
	# 				values = []
	# 		else:
	# 			key = str(specification.id)
	# 			if key in equipment.specifications.keys():
	# 				val = '%s: %s' % (specification.label, equipment.specifications[key])
	# 				val = get_paragraph(val, 6)

	# 				values.append([val,])

	# 	if len(values) > 0:
	# 		data[i].append(get_list_component(values))
	
	table = get_table(equipments, fields, col_widths)

	return [table_title, table]

def get_signatures(values_list):
	story = [Spacer(0, 2.5*cm)]

	table_style = TableStyle([
		#('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
		#('GRID',(0,0),(-1,-1), 0.25, colors.black),
		('VALIGN', (0, 0), (-1, -1), 'TOP'),
		('ALIGN', (0, 0), (-1,-1), 'CENTER'),
		('FONTSIZE', (0, 0), (-1, -1), 12),
	])

	names = []
	positions = []
	for name, position in values_list:
		names.append(name)
		pos = get_strong_text(position, 12)
		pos.style.alignment=TA_CENTER
		positions.append(pos)

	table = Table([names, positions], style=table_style, hAlign='CENTER')
	story.append(table)
	return story


def get_table_dispatch(dispatch):
	story = []
	details = dispatch.get_details()	
	for key in details:
		story.append(get_strong_text(key, 12))
		story.append(Spacer(0, 0.5*cm))
		data = [['Descripción', 'Cantidad']]
		for description, quantity in details[key]:
			data.append([description, quantity])
		data = get_styled_data(data)
		table = Table(data, [None, 3*cm], style=get_table_style(10), hAlign='CENTER')
		story.append(table)

	return story

