# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=64)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Deparment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=16)),
                ('name', models.CharField(max_length=64)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('charter', models.CharField(max_length=10)),
                ('extension', models.CharField(max_length=8, null=True, blank=True)),
                ('is_head', models.PositiveSmallIntegerField()),
                ('area', models.ForeignKey(to='structure.Area')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='employee',
            name='job',
            field=models.ForeignKey(to='structure.Job'),
        ),
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='area',
            name='deparment',
            field=models.ForeignKey(to='structure.Deparment'),
        ),
    ]
