# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ruc', models.CharField(max_length=13)),
                ('name', models.CharField(max_length=64)),
                ('representative', models.CharField(max_length=128, null=True, blank=True)),
                ('address', models.CharField(max_length=128)),
                ('city', models.CharField(max_length=32, null=True, blank=True)),
                ('cellphone', models.CharField(max_length=64, null=True, blank=True)),
                ('telephone', models.CharField(max_length=64, null=True, blank=True)),
            ],
        ),
    ]
