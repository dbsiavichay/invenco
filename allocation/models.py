from django.db import models
from structure.models import Employee
from equipment.models import Device
 
class Allocation(models.Model):
	date_joined = models.DateTimeField()
	is_active = models.BooleanField()
	employee = models.ForeignKey(Employee)
	device = models.ForeignKey(Device)

