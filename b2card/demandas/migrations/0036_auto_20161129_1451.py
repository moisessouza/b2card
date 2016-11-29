# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-29 16:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demandas', '0035_demanda_unidade_administrativa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='demanda',
            name='unidade_administrativa',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.UnidadeAdministrativa'),
        ),
    ]
