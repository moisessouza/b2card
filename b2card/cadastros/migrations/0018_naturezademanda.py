# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-23 17:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0017_fase'),
    ]

    operations = [
        migrations.CreateModel(
            name='NaturezaDemanda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
    ]
