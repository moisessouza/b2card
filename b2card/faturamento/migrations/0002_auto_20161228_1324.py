# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-28 15:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faturamento', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parcela',
            name='tipo_parcela',
        ),
        migrations.AlterField(
            model_name='medicao',
            name='quantidade_horas',
            field=models.FloatField(),
        ),
    ]