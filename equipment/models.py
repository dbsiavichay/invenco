from django.db import models
from providers.models import Provider
from django_pgjson.fields import JsonField
from datetime import date

class Trademark(models.Model):
	class Meta:
		ordering = ['name',]

	name = models.CharField(max_length=32)

	def __unicode__(self):
		return self.name

class Type(models.Model):
	class Meta:
		ordering = ['name',]

	name = models.CharField(max_length=32)
	is_part = models.BooleanField(default=False)
	specifications = JsonField(blank=True, null=True)

	def __unicode__(self):
		return self.name

class Model(models.Model):
	class Meta:
		ordering = ['type', 'trademark', 'name']

	name = models.CharField(max_length=128)
	specifications = JsonField(blank=True, null=True)
	type = models.ForeignKey(Type)
	trademark = models.ForeignKey(Trademark)

	def __unicode__(self):
		return self.name

class Device(models.Model):
	class Meta:
		ordering = ['model',]

	code = models.CharField(max_length=16, unique=True)
	serial = models.CharField(max_length=34, unique=True, blank=True, null=True)
	part = models.CharField(max_length=32, blank=True, null=True)
	state = models.CharField(max_length=16, blank=True, null=True)
	invoice = models.CharField(max_length=16, blank=True, null=True)
	date_purchase = models.DateField(blank=True, null=True)
	date_warranty = models.DateField(blank=True, null=True)
	specifications = JsonField(blank=True, null=True)
	model = models.ForeignKey(Model)
	provider = models.ForeignKey(Provider, blank=True, null=True)

	def get_state_icon(self):
		icon = 'ok-sign' if self.state == '1' else 'minus-sign' if self.state == '2' else 'remove-sign'
		return icon

	def __unicode__(self):
		return '%s %s %s | %s' % (self.model.type, self.model.trademark, self.model, self.code)
