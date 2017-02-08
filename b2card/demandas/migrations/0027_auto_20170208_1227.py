# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-08 14:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demandas', '0026_orcamento_lucro_calculado_projetado'),
    ]

    operations = [
        migrations.AddField(
            model_name='orcamento',
            name='horas_proposto',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='orcamento',
            name='lucro_calculado_proposto',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='orcamento',
            name='valor_proposto',
            field=models.FloatField(default=None, null=True),
        ),
    ]