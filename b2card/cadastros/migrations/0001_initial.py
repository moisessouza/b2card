# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-27 12:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CentroCusto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='CentroResultado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ContaGerencial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='NaturezaOperacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TipoHora',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='UnidadeAdministrativa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(default=None, max_length=10)),
                ('nome', models.CharField(default=None, max_length=30)),
            ],
        ),
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
