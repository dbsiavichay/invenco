from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
	name = models.CharField(max_length = 64)

	def __unicode__(self):
		return self.name

class Department(models.Model):
	code = models.CharField(max_length = 16)
	name = models.CharField(max_length = 64)

	def __unicode__(self):
		return self.name

class Area(models.Model):
	code = models.CharField(max_length = 16)
	name = models.CharField(max_length = 64)
	department = models.ForeignKey(Department)

	def __unicode__(self):
		return self.name

class Employee(models.Model):
	charter = models.CharField(max_length = 10)
	extension = models.CharField(max_length = 8, blank=True, null=True)
	is_head = models.PositiveSmallIntegerField()
	user = models.ForeignKey(User)
	area = models.ForeignKey(Area)
	job = models.ForeignKey(Job)