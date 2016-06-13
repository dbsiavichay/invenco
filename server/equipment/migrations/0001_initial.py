# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('providers', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=16, verbose_name=b'Codigo')),
                ('serial', models.CharField(max_length=34, unique=True, null=True, verbose_name=b'Serie', blank=True)),
                ('part', models.CharField(max_length=32, null=True, verbose_name=b'Parte', blank=True)),
                ('specifications', django_pgjson.fields.JsonField(null=True, blank=True)),
                ('state', models.CharField(max_length=16, null=True, verbose_name=b'Estado', blank=True)),
                ('invoice', models.CharField(max_length=16, null=True, verbose_name=b'Factura', blank=True)),
                ('date_purchase', models.DateField(null=True, verbose_name=b'Compra', blank=True)),
                ('date_warranty', models.DateField(null=True, verbose_name=b'Garantia', blank=True)),
            ],
            options={
                'ordering': ['model'],
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('specifications', django_pgjson.fields.JsonField(null=True, blank=True)),
            ],
            options={
                'ordering': ['type', 'trademark', 'name'],
            },
        ),
        migrations.CreateModel(
            name='Trademark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('is_part', models.BooleanField(default=False)),
                ('specifications', django_pgjson.fields.JsonField(null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='model',
            name='trademark',
            field=models.ForeignKey(to='equipment.Trademark'),
        ),
        migrations.AddField(
            model_name='model',
            name='type',
            field=models.ForeignKey(to='equipment.Type'),
        ),
        migrations.AddField(
            model_name='device',
            name='model',
            field=models.ForeignKey(verbose_name=b'Modelo', to='equipment.Model'),
        ),
        migrations.AddField(
            model_name='device',
            name='provider',
            field=models.ForeignKey(verbose_name=b'Proveedor', blank=True, to='providers.Provider', null=True),
        ),
    ]
