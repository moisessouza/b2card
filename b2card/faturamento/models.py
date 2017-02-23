# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from cadastros.models import ValorHora, PessoaJuridica
from demandas.models import Demanda, OrcamentoFase


# Create your models here.
STATUS = (
    ('PE', 'Pendente'),
    ('PA', 'Pendente aprovação'),
    ('PF', 'Pendente faturamento'),
    ('FA', 'Faturado'),
    ('PA', 'Pago')
)

class PacoteItens(models.Model):
    cliente = models.ForeignKey(PessoaJuridica, default = None, null = True)
    data_criacao = models.DateField(default=None)
    valor_total = models.FloatField(default=None)
    total_horas = models.FloatField(default=None)
    
class Parcela(models.Model):
    descricao = models.CharField(max_length = 200)
    valor_parcela = models.FloatField(max_length=30, null=True)
    status = models.CharField(max_length=2, choices=STATUS, null=True)
    data_previsto_parcela = models.DateField(null=True)
    demanda = models.ForeignKey(Demanda, null=True)
    pacote_itens = models.ForeignKey(PacoteItens, null = True, default = None)
    
class ParcelaFase(models.Model):
    parcela = models.ForeignKey(Parcela)
    fase = models.ForeignKey(OrcamentoFase)
    valor = models.FloatField(max_length=30, null=True)
    
class Medicao(models.Model):
    parcela_fase = models.ForeignKey(ParcelaFase, null=True)
    valor_hora = models.ForeignKey(ValorHora, default=None)
    quantidade_horas = models.FloatField()
    valor_total = models.FloatField()