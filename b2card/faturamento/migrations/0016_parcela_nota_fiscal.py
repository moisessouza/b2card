# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-30 13:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('faturamento', '0015_lotedespesa_motivo_despesa'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcela',
            name='nota_fiscal',
            field=models.CharField(default=None, max_length=20, null=True),
        ),
    ]
