# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('employee', models.CharField(max_length=16)),
                ('department', models.FloatField()),
                ('area', models.FloatField()),
                ('date_joined', models.DateField()),
                ('is_active', models.BooleanField()),
                ('device', models.ForeignKey(to='equipment.Device')),
            ],
        ),
    ]
