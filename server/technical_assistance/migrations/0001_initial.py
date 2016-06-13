# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('problem', models.TextField()),
                ('solution', models.TextField()),
                ('device', models.ForeignKey(to='equipment.Device')),
            ],
        ),
        migrations.CreateModel(
            name='Parts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_active', models.BooleanField()),
                ('maintenance', models.ForeignKey(to='technical_assistance.Maintenance')),
                ('part', models.ForeignKey(to='equipment.Device')),
            ],
        ),
    ]
