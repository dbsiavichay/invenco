#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from audit.mixins import AuditMixin

class Building(AuditMixin, models.Model):
    name = models.CharField(max_length=64, verbose_name='nombre')
    address = models.CharField(max_length=128, verbose_name='dirección')

    def __unicode__(self):
        return self.name

class Department(models.Model):
    code = models.FloatField(primary_key=True, db_column='coddepar')
    name = models.CharField(max_length=60, db_column='nomdepar')

    class Meta:
        managed = False
        db_table = 'departamentos'
        ordering = ['name',]

    def __unicode__(self):
        return self.name

class Section(models.Model):
    department = models.ForeignKey(Department, db_column='coddepar')
    code = models.FloatField(primary_key=True, db_column='codseccion')
    name = models.CharField(max_length=100, blank=True, null=True, db_column='nomseccion')

    class Meta:
        managed = False
        db_table = 'secciones'
        ordering = ['name',]

class Contributor(models.Model):
    charter = models.CharField(primary_key=True, max_length=15, db_column='ctrcedula')
    name = models.CharField(max_length=120, blank=True, null=True, db_column='ctrnombre')
    email = models.CharField(max_length=60, blank=True, null=True, db_column='ctremail')
    state = models.CharField(max_length=20, blank=True, null=True, db_column='ctrestado')

    class Meta:
        managed = False
        db_table = 'contribuyentes'
        ordering = ['name',]

    def __unicode__(self):
        return str(self.charter)

class Employee(models.Model):
    contributor = models.ForeignKey('Contributor', db_column='bicodcon')
    code = models.CharField(primary_key=True, max_length=2, db_column='biprvcodigo')
    department = models.FloatField(blank=True, null=True, db_column='bicoddep')
    section = models.FloatField(blank=True, null=True, db_column='bicodsec')

    class Meta:
        managed = False
        db_table = 'bicondep'
        ordering = ['contributor',]

    def __unicode__(self):
        return '%s | %s' % (self.contributor.charter, self.contributor.name)
