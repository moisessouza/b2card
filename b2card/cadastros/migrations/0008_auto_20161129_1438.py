# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-29 16:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0007_unidadeadministrativa'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidadeadministrativa',
            name='codigo',
            field=models.CharField(default=None, max_length=10),
        ),
        migrations.AlterField(
            model_name='unidadeadministrativa',
            name='nome',
            field=models.CharField(default=None, max_length=30),
        ),
    ]