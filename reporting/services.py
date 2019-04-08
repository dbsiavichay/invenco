# -*- coding: utf-8 -*-
from django.conf import settings
from os.path import join

from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.platypus import Image, Table, TableStyle, Paragraph

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
def get_strong_text(text, size=10):
	stylesheet=getSampleStyleSheet()
	bold = stylesheet['Heading5']
	bold.fontSize = size

 	return Paragraph(text, style=bold)

def get_paragraph(text, size):
	style = getSampleStyleSheet()['Normal']
	style.fontSize = size
	style.leading = size

	return Paragraph(text, style=style)

### Functions for draw tables
def get_table_style():
	style = TableStyle([
		('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
		('GRID',(0,0),(-1,-1), 0.25, colors.black),
		('VALIGN', (0, 0), (-1, -1), 'TOP'),
		('FONTSIZE', (0, 0), (-1, -1), 6),
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

def get_table_equipments(type):
	equipments = Equipment.objects.filter(model__type=type).exclude(state=10)

	if len(equipments) <= 0:
		return None

	table_title = get_table_title(type.name)
	headers = ['Marca', 'Equipo', 'Serie', 'Código','Responsable', 'Estado']
	columns_width = [1.5*cm, 3*cm,2.3*cm,1.5*cm,4*cm, 3*cm]
	fields = ('model.brand', 'model.name', 'serial', 'code', 'get_responsible', 'get_state')

	data = get_data(equipments, fields)	

	# ##Specifications
	specifications = type.type_specifications.filter(when='device')

	
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

	data = get_styled_data([headers,] + data)	
	table = Table(data, columns_width, style=get_table_style(), hAlign='LEFT')

	return [table_title, table]
