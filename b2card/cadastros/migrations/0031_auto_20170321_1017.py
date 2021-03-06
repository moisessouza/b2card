# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-21 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0030_auto_20170308_1021'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDespesa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='tipo',
            field=models.CharField(choices=[('F', 'FISICA'), ('J', 'JURIDICA')], max_length=1),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='tipo_pessoa',
            field=models.CharField(choices=[('C', 'CLIENTE'), ('F', 'FORNECEDOR'), ('A', 'AMBOS')], max_length=1),
        ),
    ]
