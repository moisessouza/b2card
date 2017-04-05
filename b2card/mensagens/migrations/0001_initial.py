# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-28 14:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cadastros', '0032_pessoajuridica_cliente_demanda'),
    ]

    operations = [
        migrations.CreateModel(
            name='Messagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('texto', models.TextField(default=None)),
                ('lido', models.NullBooleanField(default=False)),
                ('tag', models.CharField(choices=[('E', 'Exame Periodico')], default=None, max_length=1)),
                ('pessoa', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadastros.PessoaFisica')),
            ],
        ),
        migrations.CreateModel(
            name='Responsavel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(choices=[('E', 'Exame Periodico')], default=None, max_length=1)),
                ('ativo', models.NullBooleanField(default=False)),
                ('pessoa', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='cadastros.PessoaFisica')),
            ],
        ),
    ]
