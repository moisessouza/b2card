# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-12-01 12:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('demandas', '0038_demanda_unidade_administrativa'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContasReceber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_conta', models.CharField(choices=[('P', 'Parcela'), ('M', 'Medi\ufffd\ufffdo')], max_length=1, null=True)),
                ('numero_vezes', models.IntegerField()),
                ('demanda', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='demandas.Demanda')),
            ],
        ),
        migrations.CreateModel(
            name='Parcela',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.CharField(max_length=200)),
                ('valor_parcela', models.CharField(max_length=30, null=True)),
                ('numero_horas', models.IntegerField()),
                ('status', models.CharField(choices=[('PE', 'Previsto'), ('PA', 'Pendente aprova\ufffd\ufffdo'), ('PF', 'Pendente faturamento'), ('FA', 'Faturado'), ('PA', 'Pago')], max_length=2, null=True)),
                ('data_previsto_parcela', models.DateField(null=True)),
                ('contas_receber', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='faturamento.ContasReceber')),
            ],
        ),
    ]