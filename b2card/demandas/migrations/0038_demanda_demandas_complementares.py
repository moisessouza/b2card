# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-08 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demandas', '0037_auto_20170307_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='demanda',
            name='demandas_complementares',
            field=models.ManyToManyField(default=None, null=True, to='demandas.Demanda'),
        ),
    ]