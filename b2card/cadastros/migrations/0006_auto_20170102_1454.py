# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-01-02 16:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0005_auto_20170102_1354'),
    ]

    operations = [
        migrations.RenameField(
            model_name='prestador',
            old_name='dataa_ultima_avaliacao',
            new_name='data_ultima_avaliacao',
        ),
    ]
