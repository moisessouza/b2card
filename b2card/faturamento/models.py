# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from demandas.models import Demanda, Fase
from cadastros.models import ValorHora

# Create your models here.

TIPO_PARCELA = (
    ('P', 'Parcela'),
    ('M', 'Medição')
)

STATUS = (
    ('PE', 'Previsto'),
    ('PA', 'Pendente aprovação'),
    ('PF', 'Pendente faturamento'),
    ('FA', 'Faturado'),
    ('PA', 'Pago')
)
    
class Parcela(models.Model):
    descricao = models.CharField(max_length = 200)
    valor_parcela = models.FloatField(max_length=30, null=True)
    status = models.CharField(max_length=2, choices=STATUS, null=True)
    data_previsto_parcela = models.DateField(null=True)
    demanda = models.ForeignKey(Demanda, null=True)
    tipo_parcela = models.CharField(max_length=1, choices = TIPO_PARCELA, null=True)
    
class ParcelaFase(models.Model):
    parcela = models.ForeignKey(Parcela)
    fase = models.ForeignKey(Fase)
    valor = models.FloatField(max_length=30, null=True)
    
class Medicao(models.Model):
    parcela_fase = models.ForeignKey(ParcelaFase, null=True)
    valor_hora = models.ForeignKey(ValorHora, default=None)
    valor = models.FloatField()
    quantidade_horas = models.IntegerField()
    valor_total = models.FloatField()