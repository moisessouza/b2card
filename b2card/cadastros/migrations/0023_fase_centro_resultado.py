# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-02-15 13:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0022_auto_20170209_1420'),
    ]

    operations = [
        migrations.AddField(
            model_name='fase',
            name='centro_resultado',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='cadastros.CentroResultado'),
        ),
    ]
