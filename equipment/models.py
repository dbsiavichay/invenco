from django.db import models
from providers.models import Provider
from django_pgjson.fields import JsonField
from datetime import date

class Trademark(models.Model):
	name = models.CharField(max_length=32)

	def __unicode__(self):
		return self.name

class Type(models.Model):
	name = models.CharField(max_length=32)
	specifications = JsonField(blank=True, null=True)

	def __unicode__(self):
		return self.name

class Model(models.Model):
	name = models.CharField(max_length=128)
	specifications = JsonField(blank=True, null=True)
	type = models.ForeignKey(Type)
	trademark = models.ForeignKey(Trademark)

	def __unicode__(self):
		return self.name

class Device(models.Model):
	code = models.CharField(max_length=16, unique=True)
	serial = models.CharField(max_length=34, unique=True, blank=True, null=True)
	part = models.CharField(max_length=32, blank=True, null=True)
	state = models.CharField(max_length=16, blank=True, null=True)
	invoice = models.CharField(max_length=16, blank=True, null=True)
	date_purchase = models.DateField()
	date_warranty = models.DateField()
	specifications = JsonField(blank=True, null=True)
	model = models.ForeignKey(Model)
	provider = models.ForeignKey(Provider, blank=True, null=True)

	def get_state_icon(self):
		icon = 'ok-sign' if self.state == '1' else 'minus-sign' if self.state == '2' else 'remove-sign'		
		return icon

	def __unicode__(self):
		return '%s %s %s - Code: %s' % (self.model.type, self.model.trademark, self.model, self.code)
