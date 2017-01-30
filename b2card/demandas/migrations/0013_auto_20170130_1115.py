# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-30 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demandas', '0012_auto_20170127_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividade',
            name='percentual_calculado',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='atividadeprofissional',
            name='percentual_calculado',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='demanda',
            name='data_fim',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='demanda',
            name='data_inicio',
            field=models.DateField(default=None),
        ),
        migrations.AddField(
            model_name='demanda',
            name='percentual_calculado',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='faseatividade',
            name='percentual_calculado',
            field=models.IntegerField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='faseatividade',
            name='data_fim',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='faseatividade',
            name='data_inicio',
            field=models.DateField(default=None),
        ),
    ]
