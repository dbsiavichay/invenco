from django_pg import models

class Trademark(models.Model):
	name = models.CharField(max_length=32)

class Type(models.Model):
	name = models.CharField(max_length=32)
	specifications = models.JSONField()

class Model(models.Model):
	name = models.CharField(max_length=128)
	specifications = models.JSONField()
	type = models.ForeignKey(Type)
	trademark = models.ForeignKey(Trademark)

class Device(models.Model):
	code = models.CharField(max_length=16, unique=True)
	serial = models.CharField(max_length=34, unique=True, blank=True, null=True)
	part = models.CharField(max_length=32, blank=True, null=True)
	ip = models.CharField(max_length=16, blank=True, null=True)
	date_purchase = models.DateTimeField()
	date_warranty = models.DateTimeField()
	specifications = models.JSONField()
	model = models.ForeignKey(Model)
