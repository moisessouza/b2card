# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-15 14:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demandas', '0018_demanda_centro_resultado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demanda',
            name='centro_resultado',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='clientes.CentroResultado'),
        ),
    ]
