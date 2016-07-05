from django.db import models

class Provider(models.Model):
	ruc = models.CharField(max_length=13)
	name = models.CharField(max_length=64)
	representative = models.CharField(max_length=128, blank=True, null=True)
	address = models.CharField(max_length=128)
	city = models.CharField(max_length=32, blank=True, null=True)
	cellphone = models.CharField(max_length=64, blank=True, null=True)
	telephone = models.CharField(max_length=64, blank=True, null=True)

	def __unicode__(self):
		return self.name
