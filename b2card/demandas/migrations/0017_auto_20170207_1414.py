# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-07 16:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demandas', '0016_auto_20170202_1642'),
    ]

    operations = [
        migrations.AddField(
            model_name='orcamento',
            name='lucro_desejado',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='orcamento',
            name='margem_risco',
            field=models.FloatField(default=None, null=True),
        ),
    ]
