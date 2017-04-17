from __future__ import unicode_literals

from django.db import models

from stocktaking.models import Equipment, Replacement

# Create your models here.

class Fix(models.Model):
	problem = models.TextField()
	solution = models.TextField()
	observation = models.TextField()
	date_joined = models.DateTimeField(auto_now_add=True)
	equipment = models.ForeignKey(Equipment)


class Parts(models.Model):	
	quantity = models.FloatField()
	replacement = models.ForeignKey(Replacement)
	fix = models.ForeignKey(Fix)

	def __unicode__(self):
		return str(self.part)
