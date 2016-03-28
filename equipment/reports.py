from django.db import connection
from equipment.models import Type, Device
from organization.models import Department
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
from reportlab.lib.units import cm
from io import BytesIO

def get_pdf(options):
	departments=Department.objects.using('sim').all().exclude(name__icontains='jubilados')
	buff = BytesIO()
	doc = SimpleDocTemplate(buff, pagesize=landscape(A4), rightMargin=40, leftMargin=40, topMargin=20, bottomMargin=20,)
	styles = getSampleStyleSheet()
	report = []
	report.append(Paragraph("Reporte de equipos registrados", styles['Title']))

	for option in options:
		t = Type.objects.get(pk=option)
		columns_width = [s*cm for s in t.get_print_sizes()]

		report.append(Paragraph(t.name.capitalize(), styles['Heading2']))
		for department in departments:
			values = Device.objects.filter(model__type = t, allocation__is_active=True, allocation__department=department.code).order_by('allocation__area')
			if len(values) > 0:
				report.append(Paragraph(department.name, styles['Heading4']))
				headings = get_table_headings(Device, t)
				data = get_table_content(values, t)
				report.append(get_table(headings, data, columns_width))

		values = Device.objects.filter(model__type=t).exclude(allocation__is_active=True)
		if len(values) > 0:
			report.append(Paragraph('SIN ASIGNAR', styles['Heading4']))
			headings = get_table_headings(Device, t)
			data = get_table_content(values, t)
			report.append(get_table(headings, data, columns_width))

		if 'pc' in t.name.lower():
			report.append(Paragraph("Informacion adicional de pc's", styles['Heading2']))
			report.append(get_pc_stats())

	doc.build(report)
	return buff.getvalue()

def get_pcdir():
	departments=Department.objects.using('sim').all().exclude(name__icontains='jubilados')
	buff = BytesIO()
	doc = SimpleDocTemplate(buff, pagesize=A4, rightMargin=40, leftMargin=40, topMargin=20, bottomMargin=20,)
	styles = getSampleStyleSheet()
	report = []
	report.append(Paragraph("Directorio de equipos", styles['Title']))

	t = Type.objects.filter(name__icontains='pc')[0]
	columns_width = [3.5*cm, 1*cm, 1.5*cm, 1.4*cm, 1.4*cm, 1.3*cm, 1.5*cm, 1*cm, 1*cm, 1*cm, 3*cm, 2*cm]
	headings = ['Modelo', 'Codigo', 'Serie', 'Uso', 'Ip', 'Usuario', 'SO', 'Bits', 'Acc', 'Estado', 'Ubicacion', 'Responsable']

	for department in departments:
		values = Device.objects.filter(model__type = t, allocation__is_active=True, allocation__department=department.code).order_by('allocation__area')
		if len(values) > 0:
			report.append(Paragraph(department.name, styles['Heading4']))
			data = [[str(d.model), d.code, d.serial,
					 d.model.specifications['Uso'],
					 d.specifications['Ip'],
					 d.specifications['Usuario'],
					 d.specifications['Sistema Operativo'],
					 d.specifications['Bits'],
					 d.specifications['Acceso Remoto'],
					 d.state,
					 d.allocation_set.filter(is_active=True)[0].short_location()[:50],
					 d.allocation_set.filter(is_active=True)[0].short_responsible()] for d in values]
			report.append(get_table(headings, data, columns_width))

	values = Device.objects.filter(model__type=t).exclude(allocation__is_active=True)
	if len(values) > 0:
		report.append(Paragraph('SIN ASIGNAR', styles['Heading4']))
		data = [[str(d.model), d.code, d.serial,
				 d.model.specifications['Uso'],
				 d.specifications['Ip'],
				 d.specifications['Sistema Operativo'],
				 d.specifications['Bits'],
				 d.specifications['Acceso Remoto'],
				 d.state, '', ''] for d in values]
		report.append(get_table(headings, data, columns_width))

	doc.build(report)
	return buff.getvalue()

def get_table_headings(model_obj, type):
	headings = []

	for field in model_obj._meta.fields:
		if field.name.lower() != 'id':
			if field.get_internal_type() != 'JsonField':
				headings.append(field.verbose_name)
			else:
				values = get_specifications_headings(type.specifications)
				for val in values: headings.append(val)

	headings+=['Ubicacion', 'Responsable']
	return headings

def get_specifications_headings(object_keys):
	values = []
	object_keys = sorted(object_keys, key = lambda k: k['for'], reverse=True)

	for item in object_keys:
		keys = item['specification']

		for key in keys:
			if str(key) not in values:
				values.append(str(key))

		options = item['options']
		for option in options:
			if type(option).__name__ == 'dict':
				suboptions = option['suboptions']
				for suboption in suboptions:
					if str(suboption) not in values:
						values.append(str(suboption))

	return values

def get_table_content(object_list, type):
	rows = []
	specification_keys = get_specifications_headings(type.specifications)

	for object in object_list:
		row = []
		for field in object._meta.fields:
			if field.name.lower() != 'id':
				if field.get_internal_type() != 'JsonField':
					val = object.__getattribute__(field.name)
					row.append(str(val) if val is not None else '')
				else:
					for key in specification_keys:
						if object.model.specifications.has_key(key):
							row.append(str(object.model.specifications[key]))
						elif object.specifications.has_key(key):
							row.append(str(object.specifications[key]))
						else:
							row.append('')
		allocations = object.allocation_set.filter(is_active=True)
		row.append(allocations[0].short_location()[:30] if len(allocations) > 0 else '')
		row.append(allocations[0].short_responsible() if len(allocations) > 0 else 'Sin asignar')
		rows.append(row)
	return rows

def get_table(headings, data, columns_width):
	styles = getSampleStyleSheet()

	headingStyle = styles['Heading5']
	headingStyle.fontSize = 6
	headingStyle.bulletFontSize = 1

	contentStyle = styles['BodyText']
	contentStyle.fontSize = 5

	headings = [Paragraph(h, headingStyle) for h in headings]
	content = [[Paragraph(cell, contentStyle) for cell in row] for row in data]

	table = Table([headings]+content, columns_width)
	table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
							('LEFTPADDING',(0,0),(-1,-1), 3),
							('RIGHTPADDING',(0,0),(-1,-1), 3),
							('BOX', (0, 0), (-1, -1), 0.5, colors.black),
							('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
							('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))

	return table

def get_pc_stats():
	stats = []
	content = []
	count = 0

	query_with_allocations = '''SELECt d.specifications->>'Sistema Operativo' as sistema, d.specifications->>'Bits' as arquitectura, count(d.specifications->'Bits') as cantidad
		FROM equipment_device as d
		INNER JOIN equipment_model as m ON m.id = d.model_id
		INNER JOIN equipment_type as t ON t.id = m.type_id
		WHERE lower(t.name) LIKE '%pc%' AND d.specifications->>'Sistema Operativo' != ''
		GROUP BY sistema, arquitectura
		ORDER BY sistema, arquitectura;'''

	query_without_allocations = '''SELECt count(d.id) as cantidad FROM equipment_device as d
		INNER JOIN equipment_model as m ON m.id = d.model_id
		INNER JOIN equipment_type as t ON t.id = m.type_id
		WHERE lower(t.name) LIKE '%pc%' AND
		(SELECt count(*) FROM allocation_allocation WHERE device_id = d.id) <= 0;'''

	cursor = connection.cursor()
	cursor.execute(query_with_allocations)

	while True:
		t = cursor.fetchone()
		if t is None:
			break
		count += t[2]
		row = (t[0], t[1], str(t[2]))
		content.append(row)

	cursor.execute(query_without_allocations)
	t = cursor.fetchone()
	count += t[0]
	content.append(('SIN ASIGNAR', '', str(t[0])))
	content.append(('--TOTAL--', '', str(count)))

	columns_width = (3*cm, 1.5*cm, 1.2*cm, )
	headings = ['Sistema', 'Arquitectura', 'Cantidad', ]

	table = get_table(headings, content, columns_width)
	return table
