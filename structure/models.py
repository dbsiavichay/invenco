from django.db import models
from django.contrib.auth.models import User

class Job(models.Model):
	name = models.CharField(max_length = 64)

class Deparment(models.Model):
	code = models.CharField(max_length = 16)
	name = models.CharField(max_length = 64)
	date = models.DateTimeField()

class Area(models.Model):
	code = models.CharField(max_length = 16)
	name = models.CharField(max_length = 64)
	date = models.DateTimeField()
	deparment = models.ForeignKey(Deparment)

class Employee(models.Model):
	charter = models.CharField(max_length = 10)
	extension = models.CharField(max_length = 8, blank=True, null=True)
	is_head = models.PositiveSmallIntegerField()
	user = models.ForeignKey(User)
	area = models.ForeignKey(Area)
	job = models.ForeignKey(Job)


