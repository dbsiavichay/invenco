# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0003_auto_20160602_1820'),
    ]

    operations = [
        migrations.AlterField(
            model_name='model',
            name='replacements',
            field=models.ManyToManyField(related_name='replacements_rel_+', to='equipment.Model'),
        ),
    ]
