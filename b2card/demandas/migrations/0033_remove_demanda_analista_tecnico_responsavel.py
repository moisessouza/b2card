# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-15 15:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demandas', '0032_auto_20170215_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='demanda',
            name='analista_tecnico_responsavel',
        ),
    ]
