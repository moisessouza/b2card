# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-24 14:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0025_pessoafisica_unidade_administrativas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoafisica',
            name='unidade_administrativas',
            field=models.ManyToManyField(default=None, to='cadastros.UnidadeAdministrativa'),
        ),
    ]
