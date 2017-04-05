# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-07 18:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('demandas', '0017_auto_20170207_1414'),
    ]

    operations = [
        migrations.CreateModel(
            name='Despesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(default=None, max_length=200)),
                ('valor', models.FloatField(default=None)),
                ('a_faturar', models.BooleanField(default=None)),
                ('orcamento', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='demandas.Orcamento')),
            ],
        ),
    ]
