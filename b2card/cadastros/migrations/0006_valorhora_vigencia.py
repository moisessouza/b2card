# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-18 18:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0005_naturezaoperacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='ValorHora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=30)),
                ('centro_custo', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadastros.CentroCusto')),
                ('centro_resultado', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadastros.CentroResultado')),
                ('conta_gerencial', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadastros.ContaGerencial')),
                ('natureza_operacao', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadastros.NaturezaOperacao')),
                ('tipo_hora', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadastros.TipoHora')),
            ],
        ),
        migrations.CreateModel(
            name='Vigencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inicio', models.DateField()),
                ('data_fim', models.DateField()),
                ('valor', models.FloatField()),
                ('valor_hora', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadastros.ValorHora')),
            ],
        ),
    ]
