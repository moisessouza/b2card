# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-29 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0006_valorhora_vigencia'),
    ]

    operations = [
        migrations.CreateModel(
            name='UnidadeAdministrativa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=30)),
            ],
        ),
    ]