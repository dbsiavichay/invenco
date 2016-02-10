from equipment.models import Type, Device
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Table
from io import BytesIO

def get_pdf():
	buff = BytesIO()
	doc = SimpleDocTemplate(buff, pagesize=landscape(A4), rightMargin=40, leftMargin=40, topMargin=20, bottomMargin=20,)
	styles = getSampleStyleSheet()
	report = []

	report.append(Paragraph("Reporte de equipos registrados", styles['Title']))

	types = Type.objects.all()
	for type in types:
		devs = Device.objects.filter(model__type = type, model__type__is_part=False)
		heading = Paragraph(type.name.capitalize(), styles['Heading2'])
		if len(devs) > 0:
			report.append(heading)
			table = get_table(devs)
			table.setStyle(TableStyle([('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
									('FONTSIZE', (0, 1), (-1, -1), 8),
		    						('BOX', (0, 0), (-1, -1), 0.5, colors.black),
		     						('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
		     						('BACKGROUND', (0, 0), (-1, 0), colors.gray)]))

			report.append(table)

	doc.build(report)
	return buff.getvalue()

def get_table_headings(model_obj):
	headings = []

	for field in model_obj._meta.fields:
		if field.name.lower() != 'id':
			if field.get_internal_type() == 'JsonField':
				for key in model_obj.__getattribute__(field.name):
					headings.append(key)
			else:
				headings.append(field.verbose_name)

			if field.name.lower() == 'model':
				for key in model_obj.model.specifications:
					headings.append(key)
	headings+=['Ubicacion', 'Responsable']
	return headings

def get_table(obj_list):
	rows = []
	row = get_table_headings(obj_list[0])
	rows.append(row)

	for obj in obj_list:
		row = []
		for field in obj._meta.fields:
			if field.name.lower() != 'id':
				if field.get_internal_type() == 'JsonField':
					field_json = obj.__getattribute__(field.name)
					for key in field_json:
						row.append(field_json[key])
				else:
					row.append(obj.__getattribute__(field.name))

				if field.name.lower() == 'model':
					field_json = obj.__getattribute__('model').specifications
					for key in field_json:
						row.append(field_json[key])

		record = obj.allocation_set.filter(is_active=True)
		if len(record) > 0:
			record = record[0]
			row+=[record.short_location(), record.short_responsible()]
		rows.append(row)
	return Table(rows)