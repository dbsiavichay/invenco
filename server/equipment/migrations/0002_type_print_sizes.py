# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django_pgjson.fields


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='type',
            name='print_sizes',
            field=django_pgjson.fields.JsonField(null=True, blank=True),
        ),
    ]
