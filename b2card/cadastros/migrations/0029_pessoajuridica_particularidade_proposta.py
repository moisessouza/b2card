# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-07 19:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0028_pessoajuridica_forma_pagamento'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoajuridica',
            name='particularidade_proposta',
            field=models.TextField(default=None, null=True),
        ),
    ]
