# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-05 16:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faturamento', '0006_auto_20161205_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcela',
            name='numero_horas',
            field=models.IntegerField(null=True),
        ),
    ]
