# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('structure', '__first__'),
        ('equipment', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Allocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_joined', models.DateTimeField()),
                ('is_active', models.BooleanField()),
                ('device', models.ForeignKey(to='equipment.Device')),
                ('employee', models.ForeignKey(to='structure.Employee')),
            ],
        ),
    ]
