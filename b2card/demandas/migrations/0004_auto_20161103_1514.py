# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-11-03 17:14
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('demandas', '0003_auto_20161103_1444'),
    ]

    operations = [
        migrations.RenameField(
            model_name='faturamentodemanda',
            old_name='tipo_horas',
            new_name='tipo_hora',
        ),
    ]
