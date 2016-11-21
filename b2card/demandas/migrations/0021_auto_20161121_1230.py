# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-21 14:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0006_valorhora_vigencia'),
        ('demandas', '0020_auto_20161115_1602'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ItemFase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor_selecionado', models.FloatField()),
                ('quantidade_horas', models.IntegerField()),
                ('valor_total', models.FloatField()),
                ('fase', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='demandas.Fase')),
                ('valor_hora', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadastros.ValorHora')),
            ],
        ),
        migrations.CreateModel(
            name='Orcamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(default=None)),
                ('total_orcamento', models.FloatField(default=None)),
                ('centro_custo', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadastros.CentroCusto')),
                ('demanda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demandas.Demanda')),
            ],
        ),
        migrations.AddField(
            model_name='fase',
            name='orcamento',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='demandas.Orcamento'),
        ),
    ]