# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-09 16:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0021_auto_20170203_1153'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidadeadministrativa',
            name='imposto_devidos',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='unidadeadministrativa',
            name='lucro_desejado',
            field=models.FloatField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='unidadeadministrativa',
            name='margem_risco',
            field=models.FloatField(default=None, null=True),
        ),
    ]