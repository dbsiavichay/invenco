from django.db import models
from equipment.models import Device
from allocation.models import Allocation
from organization.models import Contributor

class Maintenance(models.Model):
	date = models.DateField()
	problem = models.TextField()
	solution = models.TextField()
	device = models.ForeignKey(Device)

	def responsible(self):
		allocations = Allocation.objects.filter(device=self.device, is_active=True)
		if len(allocations) > 0:
			contributor = Contributor.objects.using('sim').get(charter=allocations[0].employee)
			return contributor.name		

class Parts(models.Model):
	is_active = models.BooleanField()
	part = models.ForeignKey(Device)
	maintenance = models.ForeignKey(Maintenance)

	def __unicode__(self):
		return str(self.part)


