# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.html import format_html
from django.db import models

from audit.mixins import AuditMixin

# Create your models here.

class ProblemType(models.Model):
	name = models.CharField(max_length=32, verbose_name='nombre')

	def __unicode__(self):
		return self.name

	class Meta:
		verbose_name='tipo de problema'
		verbose_name_plural='tipos de problema'

class Ticket(models.Model):
	CREATED, OPEN, SOLVED, CLOSED, CANCELED = (1,2,3,4,5)
	
	STATUS_CHOICES = (
		(CREATED,'Creado'), (OPEN,'Abierto'), (SOLVED, 'Resuelto'), (CLOSED, 'Cerrado'),(CANCELED, 'Anulado'),
	)

	problem_type = models.ForeignKey(ProblemType, verbose_name='tipo de problema')
	equipment = models.ForeignKey('stocktaking.Equipment', verbose_name='equipo')
	problem = models.TextField(verbose_name='descripción del problema')
	status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=OPEN)
	date = models.DateTimeField(auto_now_add=True)
	user = models.ForeignKey('auth.User')

	def get_status_html(self):
		STATUS_LABELS = (
			(1,'info'), (2,'primary'), (3, 'success'), (4, 'warning'),(5, 'default')
		)

		return format_html(
            '<span class="label label-{}">{}</span>',
            dict(STATUS_LABELS).get(self.status),
            dict(self.STATUS_CHOICES).get(self.status),            
        )		

	def __unicode__(self):
		return '%s | %s' % (self.id, self.equipment)

	class Meta:
		ordering = ['-date']

class Reply(models.Model):
	description = models.TextField(verbose_name='razón')	
	date = models.DateTimeField(auto_now_add=True)
	ticket = models.OneToOneField(Ticket)