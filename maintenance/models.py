# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from stocktaking.models import Equipment

from audit.mixins import AuditMixin

# Create your models here.

class Fix(AuditMixin, models.Model):
	class Meta:
		ordering = ['-date_joined',]

	problem = models.TextField(verbose_name='problema')
	solution = models.TextField(verbose_name='solución')
	observation = models.TextField(verbose_name='observación', blank=True, null=True)
	date_joined = models.DateTimeField(auto_now_add=True)
	equipment = models.ForeignKey('stocktaking.Equipment', verbose_name='equipo')
	user = models.ForeignKey('auth.User')
	replacements = models.ManyToManyField('stocktaking.Replacement', blank=True)

	def __unicode__(self):		
		r = '%s > %s' % (self.equipment, self.problem)
		return r.upper()