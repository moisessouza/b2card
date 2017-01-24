# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-24 17:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demandas', '0004_auto_20170124_1522'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alocacaohoras',
            name='data_alocacao_milisegundos',
        ),
        migrations.RemoveField(
            model_name='alocacaohoras',
            name='horas_alocadas',
        ),
        migrations.RemoveField(
            model_name='atividadeprofissional',
            name='horas_alocadas',
        ),
        migrations.AddField(
            model_name='alocacaohoras',
            name='data_alocacao',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='alocacaohoras',
            name='horas_alocadas_milisegundos',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='atividadeprofissional',
            name='horas_alocadas_milisegundos',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
