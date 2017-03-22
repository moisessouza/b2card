# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from cadastros.models import ValorHora, PessoaJuridica, Pessoa, TipoDespesa
from demandas.models import Demanda, OrcamentoFase


# Create your models here.
STATUS = (
    ('PE', 'Pendente'),
    ('PA', 'Pendente aprovação'),
    ('PF', 'Pendente faturamento'),
    ('FA', 'Faturado'),
    ('PG', 'Pago')
)

class LoteFaturamento(models.Model):
    data_criacao = models.DateField(default=None)
    
STATUS_PACOTE = (
    ('P', 'Pendente'),
    ('E', 'Enviado'),
    ('A', 'Aceito'),
    ('R', 'Recusado'),
    ('D', 'Deletado')
)
class PacoteItens(models.Model):
    cliente = models.ForeignKey(PessoaJuridica, default = None, null = True)
    data_criacao = models.DateField(default=None)
    valor_total = models.FloatField(default=None, null=True)
    total_horas = models.FloatField(default=None, null=True)
    status = models.CharField(max_length=1, choices=STATUS, null=True)
    lote_faturamento = models.ForeignKey(LoteFaturamento, default = None, null = True)
    
class Parcela(models.Model):
    descricao = models.CharField(max_length = 200)
    valor_parcela = models.FloatField(max_length=30, null=True)
    status = models.CharField(max_length=2, choices=STATUS, null=True)
    demanda = models.ForeignKey(Demanda, null=True)
    pacote_itens = models.ForeignKey(PacoteItens, null = True, default = None)
    data_previsto_parcela = models.DateField(null=True, default = None)
    data_envio_aprovacao = models.DateField(null=True, default = None)
    data_aprovacao_faturamento = models.DateField(null=True, default = None)
    data_previsto_pagamento = models.DateField(null=True, default = None)
    data_faturamento = models.DateField(null=True, default = None)
    data_pagamento = models.DateField(null=True, default = None)
    
class ParcelaFase(models.Model):
    parcela = models.ForeignKey(Parcela)
    fase = models.ForeignKey(OrcamentoFase)
    valor = models.FloatField(max_length=30, null=True)
    
class Medicao(models.Model):
    parcela_fase = models.ForeignKey(ParcelaFase, null=True)
    valor_hora = models.ForeignKey(ValorHora, default=None)
    quantidade_horas = models.FloatField()
    valor_total = models.FloatField()

STATUS_LOTE = (
    ('PE', 'Pendente'),
    ('AP', 'Aprovado'),
    ('PG', 'Pago')
)    

class LoteDespesa(models.Model):
    demanda = models.ForeignKey(Demanda, default = None)
    pessoa = models.ForeignKey(Pessoa, default = None)
    motivo_despesa = models.CharField(max_length=30, default = None, null = True)
    status = models.CharField(max_length=2, choices=STATUS_PACOTE, default=None)
    valor_total = models.FloatField(default = None, null = True)
    data = models.DateField(default = None)
    
class ItemDespesa(models.Model):
    lote_despesa = models.ForeignKey(LoteDespesa, default = None)
    num_documento = models.CharField(max_length=100, default = None)
    valor = models.FloatField(default = None)
    data = models.DateField(default = None)
    tipo_despesa = models.ForeignKey(TipoDespesa, default = None, on_delete=models.PROTECT)
    descricao = models.TextField(default = None, null = True)
    