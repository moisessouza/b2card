# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-28 18:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0032_pessoajuridica_cliente_demanda'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoafisica',
            name='notificar_alocacao',
            field=models.NullBooleanField(),
        ),
    ]
