# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-23 17:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('faturamento', '0004_auto_20170223_1226'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LoteFaturamento',
            new_name='PacoteItens',
        ),
    ]