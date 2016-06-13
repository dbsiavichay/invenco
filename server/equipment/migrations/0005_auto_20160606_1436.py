# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0004_auto_20160602_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='type',
            name='is_part',
        ),
        migrations.AddField(
            model_name='type',
            name='usage',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
