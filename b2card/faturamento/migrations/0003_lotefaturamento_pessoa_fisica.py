# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-23 12:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0024_unidadeadministrativa_custo_operacao_hora'),
        ('faturamento', '0002_auto_20170222_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='lotefaturamento',
            name='pessoa_fisica',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadastros.PessoaFisica'),
        ),
    ]
