# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-27 15:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clientes', '0001_initial'),
        ('recursos', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atividades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao_atividade', models.CharField(max_length=30)),
                ('tipo_atividade', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Demanda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificacao_cliente', models.CharField(max_length=30)),
                ('descricao_cliente', models.CharField(max_length=30)),
                ('numero_demanda', models.CharField(max_length=30)),
                ('nomde_documento_resumido', models.CharField(max_length=30)),
                ('informacoes_nfe', models.TextField()),
                ('observacoes', models.TextField()),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clientes.Cliente')),
                ('coordenador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recursos.Funcionario')),
            ],
        ),
        migrations.CreateModel(
            name='DespesasExtras',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=30)),
                ('tipo_despesa', models.CharField(max_length=30)),
                ('valor', models.FloatField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Orcamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_orcamento', models.DateField()),
                ('unidade_administrativa', models.CharField(max_length=30)),
                ('centro_custo', models.CharField(max_length=30)),
                ('centro_resultado', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Propostas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_proposta', models.CharField(max_length=30)),
                ('eh_corrente', models.BooleanField()),
                ('demanda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demandas.Demanda')),
            ],
        ),
        migrations.AddField(
            model_name='atividades',
            name='demanda',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='demandas.Demanda'),
        ),
        migrations.AddField(
            model_name='atividades',
            name='responsavel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recursos.Funcionario'),
        ),
    ]
