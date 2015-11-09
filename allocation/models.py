from django.db import models
from equipment.models import Device
 
class Allocation(models.Model):
	employee = models.CharField(max_length=16)
	department = models.CharField(max_length=64)
	area = models.CharField(max_length=128)
	date_joined = models.DateField()
	is_active = models.BooleanField()
	device = models.ForeignKey(Device)

