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
    
class Proposta(models.Model):
    data_recimento_solicitacao = models.DateField()
    data_limite_entrega = models.DateField(null=True)
    data_real_entrega = models.DateField(null=True)
    numerdo_proposta = models.CharField(max_length = 30, null=True)
    data_aprovacao = models.DateField(null=True)
    empresa_ganhadora = models.CharField(max_length = 30, null=True)
    total_horas_ganhadora = models.IntegerField(null=True)
    demanda = models.ForeignKey(Demanda, null=True)

SIM_NAO = (
    ('S', 'Sim'),
    ('N', 'Não')
)

class Tarefa(models.Model):
    descricao = models.TextField()
    analista_tecnico_responsavel = models.ForeignKey(Funcionario, null=True, related_name="%(app_label)s_%(class)s_related", related_query_name="%(app_label)s_%(class)ss")
    responsavel = models.ForeignKey(Funcionario, null = True)
    analise_inicio = models.DateField(null = True)
    analise_fim = models.DateField(null = True)
    analise_fim_real = models.DateField(null = True)
    densenvolvimento_inicio = models.DateField(null = True)
    desenvolvimento_fim = models.DateField(null = True)
    desenvolvimento_fim_real= models.DateField(null = True)
    homologacao_possui_sit = models.CharField(null = True, max_length=1, choices=SIM_NAO)
    homologacao_inicio = models.DateField(null = True)
    homologacao_fim = models.DateField(null = True)
    homologacao_fim_real = models.DateField(null = True)
    forecast = models.CharField(null = True, max_length=30)
    aceite = models.CharField(null = True, max_length=1, choices=SIM_NAO)
    evidencias = models.CharField(null = True, max_length=30)
    implantacao_producao = models.DateField(null = True)
    implantacao_in_loco = models.CharField(null = True, max_length=1, choices=SIM_NAO)
    demanda = models.ForeignKey(Demanda, null=True)
    
class Observacao(models.Model):
    observacao = models.CharField(max_length=100)
    data_observacao = models.DateField()
    demanda = models.ForeignKey(Demanda, null=True)