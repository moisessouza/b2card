# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-21 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mensagens', '0006_auto_20170403_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mensagem',
            name='tag',
            field=models.CharField(choices=[('E', 'Exame Periodico'), ('A', 'Alocacao de horas'), ('N', 'Aniversarios'), ('D', 'Nao lancamento dois dias'), ('F', 'Fim de fase'), ('R', 'Renegociacao'), ('P', 'Propostas pendentes'), ('G', 'Pagamento de nota'), ('M', 'Mensagem avulsa'), ('T', 'Tarefas')], default=None, max_length=1),
        ),
        migrations.AlterField(
            model_name='responsavel',
            name='tag',
            field=models.CharField(choices=[('E', 'Exame Periodico'), ('A', 'Alocacao de horas'), ('N', 'Aniversarios'), ('D', 'Nao lancamento dois dias'), ('F', 'Fim de fase'), ('R', 'Renegociacao'), ('P', 'Propostas pendentes'), ('G', 'Pagamento de nota'), ('M', 'Mensagem avulsa'), ('T', 'Tarefas')], default=None, max_length=1),
        ),
    ]
