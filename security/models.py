from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
	charter = models.CharFiel(max_lenght=16, unique=True)
	avatar = models.ImageField(upload_to='avatares', blank=True, null=True)
	user = models.OneToOneField(User)
