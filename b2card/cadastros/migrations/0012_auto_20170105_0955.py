# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-05 11:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0011_auto_20170104_1348'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestador',
            name='data_fim',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='prestador',
            name='data_inicio',
            field=models.DateField(default=None),
        ),
    ]