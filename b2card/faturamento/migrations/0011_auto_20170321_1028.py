# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-21 13:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0031_auto_20170321_1017'),
        ('demandas', '0039_auto_20170308_1427'),
        ('faturamento', '0010_auto_20170315_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemDespesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_documento', models.CharField(default=None, max_length=100)),
                ('valor', models.FloatField(default=None)),
                ('data', models.DateField(default=None)),
                ('descricao', models.TextField(default=None, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoteDespesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(default=None)),
                ('demanda', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='demandas.Demanda')),
                ('pessoa', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadastros.Pessoa')),
            ],
        ),
        migrations.AddField(
            model_name='itemdespesa',
            name='lote_despesa',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='faturamento.LoteDespesa'),
        ),
        migrations.AddField(
            model_name='itemdespesa',
            name='tipo_despesa',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadastros.TipoDespesa'),
        ),
    ]
