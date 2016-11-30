from __future__ import unicode_literals

from django.db import models
from demandas.models import Demanda
from cadastros.models import CentroResultado, ValorHora

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

class ContasReceber(models.Model):
    tipo_conta = models.CharField(max_length=1, choices=TIPO_CONTA, null=True)
    numero_vezes = models.IntegerField()
    demanda = models.ForeignKey(Demanda, null=True)    
    
class Parcela(models.Model):
    descricao = models.CharField(max_length = 200)
    numero_nota = models.CharField(max_length = 30, default=None)
    valor_parcela = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=2, choices=STATUS, null=True)
    data_previsto_faturamento = models.DateField(null=True)
    contas_receber = models.ForeignKey(ContasReceber, default=None, null=True)

class ParcelaValorHora(models.Model):
    valor_hora = models.ForeignKey(ValorHora, default=None, null=True)
    valor = models.FloatField()
    numero_horas = models.IntegerField()
    valor_total = models.FloatField()
    parcela = models.ForeignKey(Parcela, default=None, null=None)
    
class ParcelaCentroResultado (models.Model):
    centro_resultado = models.ForeignKey(CentroResultado, default=None, null=True)
    numero_horas = models.IntegerField()
    valor_total = models.FloatField()
    parcela = models.ForeignKey(Parcela, default=None, null=None)



    