# -*- coding: utf-8 -*-
from django.db import models
from recursos.models import Funcionario
from clientes.models import Cliente, TipoValorHora
from datetime import datetime  

# Create your models here.

STATUS = (
    ('P', 'Pendente'),
    ('A', 'Aprovado'),
    ('R', 'Reprovado'),
)

TIPO_DEMANDA = (
    ('D','Desenvolvimento'), 
    ('H','Homologação'), 
    ('C','Consultoria'), 
    ('A','Alocação')
)

STATUS_DEMANDA = (
    ('O','Em orçamentação'), 
    ('A','Aguardando aprovação'), 
    ('N','Não aprovada'), 
    ('C','Cancelada'), 
    ('H','Em homologação'), 
    ('I','Implantada'), 
    ('D','Em desenvolvimento')
)

class Demanda(models.Model):
    titulo = models.CharField(max_length=30, default=None)
    cliente = models.ForeignKey(Cliente, blank=False)
    identificacao = models.CharField(max_length=30,default=None)
    descricao = models.TextField(default=None)
    tipo_demanda = models.CharField(max_length=1, choices=TIPO_DEMANDA, null=True)
    status_demanda = models.CharField(max_length=1, choices=STATUS_DEMANDA, null=True)
    codigo_cri = models.CharField(max_length=12, null=True)
    
class FaturamentoDemanda(models.Model):
    descricao = models.CharField(max_length = 30)
    data = models.DateField(null=True)
    tipo_hora = models.ForeignKey(TipoValorHora, null=True)
    valor_hora = models.CharField(max_length=30, null=True)
    quantidade_horas = models.IntegerField(null=True)
    valor_faturamento = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=1, choices=STATUS, null=True)
    data_envio_aprovacao = models.DateField(null=True)
    data_aprovacao_fatura = models.DateField(null=True)
    data_fatura = models.DateField(null=True)
    demanda = models.ForeignKey(Demanda, null=True)