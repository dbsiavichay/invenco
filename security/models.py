#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	is_practicing = models.BooleanField(default=False, verbose_name='es practicante?')
	institution = models.CharField(max_length=128, blank=True, verbose_name='institución')
	avatar = models.ImageField(upload_to='avatares', blank=True, null=True)
	user = models.OneToOneField(User, verbose_name='usuario')

	def __unicode__(self):
		return self.user.get_full_name()
