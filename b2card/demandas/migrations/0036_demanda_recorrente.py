# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-17 17:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('demandas', '0035_auto_20170215_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='demanda',
            name='recorrente',
            field=models.NullBooleanField(default=None),
        ),
    ]
