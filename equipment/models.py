from django.db import models
from jsonfield import JSONField

class Trademark(models.Model):
	name = models.CharField(max_length=32)

	def __unicode__(self):
		return self.name

class Type(models.Model):
	name = models.CharField(max_length=32)
	specifications = JSONField(blank=True, null=True)

	def __unicode__(self):
		return self.name

class Model(models.Model):
	name = models.CharField(max_length=128)
	specifications = JSONField(blank=True, null=True)
	type = models.ForeignKey(Type)
	trademark = models.ForeignKey(Trademark)

	def __unicode__(self):
		return self.name

class Device(models.Model):
	code = models.CharField(max_length=16, unique=True)
	serial = models.CharField(max_length=34, unique=True, blank=True, null=True)
	part = models.CharField(max_length=32, blank=True, null=True)
	ip = models.CharField(max_length=16, blank=True, null=True)
	date_purchase = models.DateTimeField()
	date_warranty = models.DateTimeField()
	specifications = JSONField(blank=True, null=True)
	model = models.ForeignKey(Model)
