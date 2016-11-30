# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-29 16:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0008_auto_20161129_1438'),
        ('demandas', '0034_remove_orcamento_centro_custo'),
    ]

    operations = [
        migrations.AddField(
            model_name='demanda',
            name='unidade_administrativa',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.UnidadeAdministrativa'),
        ),
    ]