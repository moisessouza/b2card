# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-12 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0016_prestador_pessoa_juridica'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(default=None, max_length=100)),
            ],
        ),
    ]
