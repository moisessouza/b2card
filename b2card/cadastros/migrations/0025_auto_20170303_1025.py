# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-03 13:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0024_unidadeadministrativa_custo_operacao_hora'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoafisica',
            name='categoria_doc_militar',
            field=models.CharField(default=None, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='pessoafisica',
            name='doc_militar',
            field=models.CharField(default=None, max_length=30, null=True),
        ),
    ]
