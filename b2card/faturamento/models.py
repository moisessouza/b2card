# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from demandas.models import Demanda

# Create your models here.

TIPO_CONTA = (
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
    numero_horas = models.FloatField(null=True)
    status = models.CharField(max_length=2, choices=STATUS, null=True)
    data_previsto_parcela = models.DateField(null=True)
    demanda = models.ForeignKey(Demanda, null=True)