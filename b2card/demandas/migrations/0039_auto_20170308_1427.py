# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-08 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demandas', '0038_demanda_demandas_complementares'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demanda',
            name='demandas_complementares',
            field=models.ManyToManyField(default=None, to='demandas.Demanda'),
        ),
    ]
