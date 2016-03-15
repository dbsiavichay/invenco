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
		if 'pc' in option.lower():
			report.append(Paragraph("Pc's", styles['Heading2']))
			for department in departments:
				report.append(Paragraph(department.name, styles['Heading4']))
				report.append(get_table_pcs(department.code))
			report.append(Paragraph("Informacion adicional de pc's", styles['Heading2']))
			report.append(get_table_pcs_stats())
		elif 'monitor' in option.lower():
			report.append(Paragraph("Monitores", styles['Heading2']))
			for department in departments:
				report.append(Paragraph(department.name, styles['Heading4']))
				report.append(get_table_displays(department.code))
		elif 'mouse' in option.lower():
			report.append(Paragraph("Mouses", styles['Heading2']))
			for department in departments:
				report.append(Paragraph(department.name, styles['Heading4']))
				report.append(get_table_mouses(department.code))
		elif 'teclado' in option.lower():
			report.append(Paragraph("Teclados", styles['Heading2']))
			for department in departments:
				report.append(Paragraph(department.name, styles['Heading4']))
				report.append(get_table_keyboards(department.code))
		elif 'regulador' in option.lower():
			report.append(Paragraph("Reguladores", styles['Heading2']))
			for department in departments:
				report.append(Paragraph(department.name, styles['Heading4']))
				report.append(get_table_regulators(department.code))
		elif 'impresora' in option.lower():
			report.append(Paragraph("Impresoras", styles['Heading2']))
			for department in departments:
				report.append(Paragraph(department.name, styles['Heading4']))
				report.append(get_table_printers(department.code))
		else:
			report.append(Paragraph("Escanners", styles['Heading2']))
			for department in departments:
				report.append(Paragraph(department.name, styles['Heading4']))
				report.append(get_table_scanners(department.code))

	doc.build(report)
	return buff.getvalue()

def get_table_pcs(department):
	data = Device.objects.filter(model__type__name__icontains = 'pc', allocation__is_active=True, allocation__department=department).order_by('allocation__area')

	columns_width = (2.5*cm, 1.7*cm, 1*cm, 1.5*cm, 1.5*cm, 1.7*cm, 0.8*cm, 1*cm,
					1.2*cm, 1.2*cm, 1.5*cm, 1*cm, 1.4*cm, 1.3*cm, 1*cm, 1*cm,
					1.1*cm, 1.2*cm, 1.2*cm, 2*cm, 1.6*cm,)

	headings = ['Modelo', 'Proveedor', 'Codigo', 'Serie', 'Parte', 'Procesador',
				'Disco', 'Ram', 'Unidad Optica', 'Unidad Lectora', 'Sistema Operativo',
				'Bits', 'Ip', 'Usuario', 'Acceso Remoto', 'Estado',
				'Factura', 'Compra', 'Garantia', 'Ubicacion', 'Responsable']

	content = [[d.model.__unicode__() if d.model is not None else '',
				d.provider.__unicode__() if d.provider is not None else '', d.code, d.serial, d.part,
				d.specifications['Procesador'] if d.specifications.has_key('Procesador') else '...',
				d.specifications['Disco']if d.specifications.has_key('Disco') else '...',
				d.specifications['Ram'] if d.specifications.has_key('Ram') else '...',
				d.specifications['Unidad Optica'] if d.specifications.has_key('Unidad Optica') else '...',
				d.specifications['Unidad Lectora'] if d.specifications.has_key('Unidad Lectora') else '...',
				d.specifications['Sistema Operativo'] if d.specifications.has_key('Sistema Operativo') else '...',
				d.specifications['Bits'] if d.specifications.has_key('Bits') else '...',
				d.specifications['Ip'] if d.specifications.has_key('Ip') else '...',
				d.specifications['Usuario'].lower() if d.specifications.has_key('Usuario') else '...',
				d.specifications['Acceso Remoto'] if d.specifications.has_key('Acceso Remoto') else '...',
				d.state, d.invoice,
				d.date_purchase.__str__() if d.date_purchase is not None else '',
				d.date_warranty.__str__() if d.date_purchase is not None else '',
				d.allocation_set.filter(is_active=True)[0].short_location()[:40] if len(d.allocation_set.filter(is_active=True)) > 0 else 'N/A',
				d.allocation_set.filter(is_active=True)[0].short_responsible() if len(d.allocation_set.filter(is_active=True)) > 0 else 'No asignado'] for d in data]

	table = get_table(headings, content, columns_width)
	return table

def get_table_pcs_stats():
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

def get_table_printers(department):
	data = Device.objects.filter(model__type__name__icontains = 'impresora', allocation__is_active=True, allocation__department=department).order_by('allocation__area')

	columns_width = (2.5*cm, 1.7*cm, 1*cm, 1.5*cm, 1.5*cm, 1.5*cm, 1.4*cm, 1*cm,
					1.2*cm, 1.2*cm, 1.5*cm, 1.4*cm, 1*cm, 1.1*cm, 1.2*cm, 1.2*cm,
					2*cm, 1.6*cm,)

	headings = ['Modelo', 'Proveedor', 'Codigo', 'Serie', 'Parte', 'Tipo', 'Suministro',
	 			'Negro', 'Cyan', 'Magenta', 'Amarillo', 'Ip', 'Estado',
				'Factura', 'Compra', 'Garantia', 'Ubicacion', 'Responsable']

	content = [[d.model.__unicode__() if d.model is not None else '',
				d.provider.__unicode__() if d.provider is not None else '', d.code, d.serial, d.part,
				d.model.specifications['Tipo'] if d.model.specifications.has_key('Tipo') else '...',
				d.model.specifications['Suministro']if d.model.specifications.has_key('Suministro') else '...',
				d.model.specifications['Cart. Negro'] if d.model.specifications.has_key('Cart. Negro') else '...',
				d.model.specifications['Cart. Cyan'] if d.model.specifications.has_key('Cart. Cyan') else '...',
				d.model.specifications['Cart. Magenta'] if d.model.specifications.has_key('Cart. Magenta') else '...',
				d.model.specifications['Cart. Amarillo'] if d.model.specifications.has_key('Cart. Amarillo') else '...',
				d.specifications['Ip'] if d.specifications.has_key('Ip') else '...',
				d.state, d.invoice,
				d.date_purchase.__str__() if d.date_purchase is not None else '',
				d.date_warranty.__str__() if d.date_purchase is not None else '',
				d.allocation_set.filter(is_active=True)[0].short_location()[:40] if len(d.allocation_set.filter(is_active=True)) > 0 else 'N/A',
				d.allocation_set.filter(is_active=True)[0].short_responsible() if len(d.allocation_set.filter(is_active=True)) > 0 else 'No asignado'] for d in data]

	table = get_table(headings, content, columns_width)
	return table

def get_table_displays(department):
	data = Device.objects.filter(model__type__name__icontains = 'monitor', allocation__is_active=True, allocation__department=department).order_by('allocation__area')

	columns_width = (2.5*cm, 1.7*cm, 1*cm, 1.5*cm, 1.5*cm, 1.1*cm, 1.4*cm, 1*cm,
					1.1*cm, 1.2*cm, 1.2*cm, 2*cm, 1.6*cm,)

	headings = ['Modelo', 'Proveedor', 'Codigo', 'Serie', 'Parte', 'Tipo', 'Dimension', 'Estado',
				'Factura', 'Compra', 'Garantia', 'Ubicacion', 'Responsable']

	content = [[d.model.__unicode__() if d.model is not None else '',
				d.provider.__unicode__() if d.provider is not None else '', d.code, d.serial, d.part,
				d.model.specifications['Tipo'] if d.model.specifications.has_key('Tipo') else '...',
				d.model.specifications['Dimension']if d.model.specifications.has_key('Dimension') else '...',
				d.state, d.invoice,
				d.date_purchase.__str__() if d.date_purchase is not None else '',
				d.date_warranty.__str__() if d.date_purchase is not None else '',
				d.allocation_set.filter(is_active=True)[0].short_location()[:40] if len(d.allocation_set.filter(is_active=True)) > 0 else 'N/A',
				d.allocation_set.filter(is_active=True)[0].short_responsible() if len(d.allocation_set.filter(is_active=True)) > 0 else 'No asignado'] for d in data]

	table = get_table(headings, content, columns_width)
	return table

def get_table_mouses(department):
	data = Device.objects.filter(model__type__name__icontains = 'mouse', allocation__is_active=True, allocation__department=department).order_by('allocation__area')

	columns_width = (2.5*cm, 1.7*cm, 1*cm, 1.5*cm, 1.5*cm, 1.2*cm, 1*cm,
					1.1*cm, 1.2*cm, 1.2*cm, 2*cm, 1.6*cm,)

	headings = ['Modelo', 'Proveedor', 'Codigo', 'Serie', 'Parte', 'Conector', 'Estado',
				'Factura', 'Compra', 'Garantia', 'Ubicacion', 'Responsable']

	content = [[d.model.__unicode__() if d.model is not None else '',
				d.provider.__unicode__() if d.provider is not None else '', d.code, d.serial, d.part,
				d.model.specifications['Conector'] if d.model.specifications.has_key('Conector') else '...',
				d.state, d.invoice,
				d.date_purchase.__str__() if d.date_purchase is not None else '',
				d.date_warranty.__str__() if d.date_purchase is not None else '',
				d.allocation_set.filter(is_active=True)[0].short_location()[:40] if len(d.allocation_set.filter(is_active=True)) > 0 else 'N/A',
				d.allocation_set.filter(is_active=True)[0].short_responsible() if len(d.allocation_set.filter(is_active=True)) > 0 else 'No asignado'] for d in data]

	table = get_table(headings, content, columns_width)
	return table

def get_table_keyboards(department):
	data = Device.objects.filter(model__type__name__icontains = 'teclado', allocation__is_active=True, allocation__department=department).order_by('allocation__area')

	columns_width = (2.5*cm, 1.7*cm, 1*cm, 1.5*cm, 1.5*cm, 1.2*cm, 1*cm,
					1.1*cm, 1.2*cm, 1.2*cm, 2*cm, 1.6*cm,)

	headings = ['Modelo', 'Proveedor', 'Codigo', 'Serie', 'Parte', 'Conector', 'Estado',
				'Factura', 'Compra', 'Garantia', 'Ubicacion', 'Responsable']

	content = [[d.model.__unicode__() if d.model is not None else '',
				d.provider.__unicode__() if d.provider is not None else '', d.code, d.serial, d.part,
				d.model.specifications['Conector'] if d.model.specifications.has_key('Conector') else '...',
				d.state, d.invoice,
				d.date_purchase.__str__() if d.date_purchase is not None else '',
				d.date_warranty.__str__() if d.date_purchase is not None else '',
				d.allocation_set.filter(is_active=True)[0].short_location()[:40] if len(d.allocation_set.filter(is_active=True)) > 0 else 'N/A',
				d.allocation_set.filter(is_active=True)[0].short_responsible() if len(d.allocation_set.filter(is_active=True)) > 0 else 'No asignado'] for d in data]

	table = get_table(headings, content, columns_width)
	return table

def get_table_regulators(department):
	data = Device.objects.filter(model__type__name__icontains = 'regulador', allocation__is_active=True, allocation__department=department).order_by('allocation__area')

	columns_width = (2.5*cm, 1.7*cm, 1*cm, 1.5*cm, 1.5*cm, 1*cm,
					1.1*cm, 1.2*cm, 1.2*cm, 2*cm, 1.6*cm,)

	headings = ['Modelo', 'Proveedor', 'Codigo', 'Serie', 'Parte', 'Estado',
				'Factura', 'Compra', 'Garantia', 'Ubicacion', 'Responsable']

	content = [[d.model.__unicode__() if d.model is not None else '',
				d.provider.__unicode__() if d.provider is not None else '', d.code, d.serial, d.part,
				d.state, d.invoice,
				d.date_purchase.__str__() if d.date_purchase is not None else '',
				d.date_warranty.__str__() if d.date_purchase is not None else '',
				d.allocation_set.filter(is_active=True)[0].short_location()[:40] if len(d.allocation_set.filter(is_active=True)) > 0 else 'N/A',
				d.allocation_set.filter(is_active=True)[0].short_responsible() if len(d.allocation_set.filter(is_active=True)) > 0 else 'No asignado'] for d in data]

	table = get_table(headings, content, columns_width)
	return table

def get_table_scanners(department):
	data = Device.objects.filter(model__type__name__icontains = 'scan', allocation__is_active=True, allocation__department=department).order_by('allocation__area')

	columns_width = (2.5*cm, 1.7*cm, 1*cm, 1.5*cm, 1.5*cm, 1*cm,
					1.1*cm, 1.2*cm, 1.2*cm, 2*cm, 1.6*cm,)

	headings = ['Modelo', 'Proveedor', 'Codigo', 'Serie', 'Parte', 'Estado',
				'Factura', 'Compra', 'Garantia', 'Ubicacion', 'Responsable']

	content = [[d.model.__unicode__() if d.model is not None else '',
				d.provider.__unicode__() if d.provider is not None else '', d.code, d.serial, d.part,
				d.state, d.invoice,
				d.date_purchase.__str__() if d.date_purchase is not None else '',
				d.date_warranty.__str__() if d.date_purchase is not None else '',
				d.allocation_set.filter(is_active=True)[0].short_location()[:40] if len(d.allocation_set.filter(is_active=True)) > 0 else 'N/A',
				d.allocation_set.filter(is_active=True)[0].short_responsible() if len(d.allocation_set.filter(is_active=True)) > 0 else 'No asignado'] for d in data]

	table = get_table(headings, content, columns_width)
	return table

def get_table_headings(model_obj):
	headings = []

	styles = getSampleStyleSheet()
	paragraphStyle = styles['Normal']
	paragraphStyle.fontSize = 6

	for field in model_obj._meta.fields:
		if field.name.lower() != 'id':
			if field.get_internal_type() == 'JsonField':
				for key in model_obj.__getattribute__(field.name):
					headings.append(Paragraph(key, paragraphStyle))
			else:
				headings.append(Paragraph(field.verbose_name, paragraphStyle))

			if field.name.lower() == 'model':
				for key in model_obj.model.specifications:
					headings.append(Paragraph(key, paragraphStyle))
	headings+=[Paragraph('Ubicacion', paragraphStyle), Paragraph('Responsable', paragraphStyle)]
	return tuple(headings)

def get_table_content(obj_list):
	rows = row =  []

	styles = getSampleStyleSheet()
	paragraphStyle = styles['Normal']
	paragraphStyle.fontSize = 5

	for obj in obj_list:
		row = []
		val = None
		for field in obj._meta.fields:
			if field.name.lower() != 'id':
				if field.get_internal_type() == 'JsonField':
					field_json = obj.__getattribute__(field.name)
					for key in field_json:
						row.append(Paragraph(field_json[key], paragraphStyle))
				elif field.get_internal_type() == 'ForeignKey':
					if field.name.lower() == 'model':
						field_json = obj.__getattribute__('model').specifications
						for key in field_json:
							row.append(Paragraph(field_json[key], paragraphStyle))
					else:
						value = obj.__getattribute__(field.name)
						val = value.__unicode__() if value is not None else ''
				elif field.get_internal_type() == 'DateField':
					value = obj.__getattribute__(field.name)
					val = value.__str__() if value is not None else ''
				else:
					value = obj.__getattribute__(field.name)
					val = val if val is not None else ''

				print val
				if val is not None: row.append(Paragraph(val, paragraphStyle))

		#Data for location and responsible
		data = obj.allocation_set.filter(is_active=True)
		if len(data) > 0:
			data = data[0]
			row+=[Paragraph(data.short_location(), paragraphStyle), Paragraph(data.short_responsible(), paragraphStyle)]
		rows.append(row)
		print len(row)
		print '---------------------------------'

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
