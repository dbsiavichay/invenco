# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0002_type_print_sizes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Replacement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('unit_price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('total_price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('stock', models.DecimalField(max_digits=7, decimal_places=2)),
            ],
        ),
        migrations.AddField(
            model_name='device',
            name='observation',
            field=models.TextField(null=True, verbose_name=b'Observaciones', blank=True),
        ),
        migrations.AddField(
            model_name='model',
            name='part_number',
            field=models.CharField(max_length=32, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='model',
            name='replacements',
            field=models.ManyToManyField(related_name='replacements_rel_+', null=True, to='equipment.Model', blank=True),
        ),
        migrations.AddField(
            model_name='replacement',
            name='model',
            field=models.ForeignKey(to='equipment.Model'),
        ),
    ]
