# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-15 14:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0004_centroresultado'),
        ('demandas', '0017_demanda_data_aprovacao_demanda'),
    ]

    operations = [
        migrations.AddField(
            model_name='demanda',
            name='centro_resultado',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='clientes.CentroResultado'),
            preserve_default=False,
        ),
    ]