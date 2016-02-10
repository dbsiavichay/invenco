from django.db import models
from equipment.models import Device
from organization.models import Contributor, Department, Section

class Allocation(models.Model):
	employee = models.CharField(max_length=16)
	department = models.FloatField()
	area = models.FloatField()
	date_joined = models.DateField()
	is_active = models.BooleanField()
	device = models.ForeignKey(Device)

	def location(self):
		department = Department.objects.using('sim').get(code=self.department)
		area = Section.objects.using('sim').filter(code=self.area, department=self.department)[0]
		return '%s | %s' % (department.name, area.name)

	def responsible(self):
		contributor = Contributor.objects.using('sim').get(charter=self.employee)
		return contributor.name

	def short_responsible(self):
		responsible = self.responsible()
		arr = responsible.split()
		return '%s %s' % (arr[2].capitalize(), arr[0].capitalize())

	def short_location(self):
		#department = Department.objects.using('sim').get(code=self.department)
		area = Section.objects.using('sim').filter(code=self.area, department=self.department)[0]

		#strdepartment = ' '.join([word.capitalize() for word in department.name.split()])
		strarea = ' '.join([word.capitalize() for word in area.name.split()])
		#return '%s | %s' % (strdepartment, strarea)
		return strarea
