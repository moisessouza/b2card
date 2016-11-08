# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-11-08 11:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recursos', '0008_auto_20161031_1606'),
        ('demandas', '0011_observacao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ocorrencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_ocorrencia', models.CharField(choices=[(b'E', b'Erro'), (b'S', b'Erro de Especifica\xc3\xa7\xc3\xa3o'), (b'F', b'Fora do escopo inicial do projeto')], max_length=1)),
                ('descricao', models.CharField(max_length=100)),
                ('nome_solicitante', models.CharField(max_length=30)),
                ('data_solicitacao', models.DateField()),
                ('data_prevista_conclusao', models.DateField()),
                ('etapa', models.CharField(choices=[(b'C', b'Conclu\xc3\xaddo'), (b'A', b'Aguardando an\xc3\xa1lise'), (b'E', b'Em avalia\xc3\xa7\xc3\xa3o')], max_length=1)),
                ('descricao_motivo', models.TextField()),
                ('observacao', models.TextField()),
                ('demanda', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='demandas.Demanda')),
                ('responsavel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='recursos.Funcionario')),
            ],
        ),
    ]
