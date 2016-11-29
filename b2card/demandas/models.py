# -*- coding: utf-8 -*-
from django.db import models
from recursos.models import Funcionario
from clientes.models import Cliente
from datetime import datetime
from cadastros.models import CentroCusto, ValorHora, CentroResultado

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
    cliente = models.ForeignKey(Cliente, blank=False)
    nome_demanda = models.CharField(max_length=30,default=None)
    descricao = models.TextField(default=None, null=True)
    status_demanda = models.CharField(max_length=1, choices=STATUS_DEMANDA, null=True)
    codigo_demanda = models.CharField(max_length=12, null=True)
    
class Atividade(models.Model):
    titulo = models.CharField(max_length=100)
    responsavel = models.ForeignKey(Funcionario, default=None)
    centro_resultado = models.ForeignKey(CentroResultado, default=None)
    horas_previstas = models.IntegerField()
    demanda = models.ForeignKey(Demanda)
    
class FaturamentoDemanda(models.Model):
    descricao = models.CharField(max_length = 200)
    numero_nota = models.CharField(max_length = 30, default=None)
    valor_total_faturamento = models.CharField(max_length=30, null=True)
    status = models.CharField(max_length=1, choices=STATUS, null=True)
    data_envio_aprovacao = models.DateField(null=True)
    data_previsto_faturamento = models.DateField(null=True)
    data_previsto_pagamento = models.DateField(null=True)
    data_pagamento = models.DateField(null=True)
    data_fatura = models.DateField(null=True)
    demanda = models.ForeignKey(Demanda, null=True)
    
class ValorHoraFaturamento(models.Model):
    valor_hora = models.ForeignKey(ValorHora, null=True)
    valor = models.FloatField(null=True)
    quantidade_horas = models.IntegerField(null=True)
    valor_faturamento = models.CharField(max_length=30, null=True)
    faturamento_demanda = models.ForeignKey(FaturamentoDemanda, null=True, on_delete=models.CASCADE) 
    
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
    observacao = models.TextField()
    data_observacao = models.DateField()
    demanda = models.ForeignKey(Demanda, null=True)
    
TIPOS_OCORRENCIA = (
    ('E', 'Erro'),
    ('S', 'Erro de Especificação'),
    ('F', 'Fora do escopo inicial do projeto')
)

ETAPA = (
    ('C', 'Concluído'),
    ('A', 'Aguardando análise'),
    ('E', 'Em avaliação')
)
    
class Ocorrencia(models.Model):
    tipo_ocorrencia = models.CharField(max_length=1, choices=TIPOS_OCORRENCIA)
    descricao = models.CharField(max_length=100)
    nome_solicitante = models.CharField(max_length = 30)
    data_solicitacao = models.DateField(null=True)
    data_prevista_conclusao = models.DateField(null=True)
    etapa = models.CharField(max_length=1, choices = ETAPA)
    responsavel = models.ForeignKey(Funcionario, null=True)
    descricao_motivo = models.TextField()
    observacao = models.TextField()
    demanda = models.ForeignKey(Demanda, null=True)
    
class Orcamento(models.Model):
    demanda = models.ForeignKey(Demanda)
    descricao = models.TextField(null=True, default = None)
    total_orcamento = models.FloatField(default = None, null=True)
    
class Fase(models.Model):
    descricao = models.CharField(max_length=100)
    valor_total = models.FloatField(default = None)
    orcamento = models.ForeignKey(Orcamento, default=None)
    
class ItemFase(models.Model):
    fase = models.ForeignKey(Fase, default = None)
    valor_hora = models.ForeignKey(ValorHora, default=None)
    valor_selecionado = models.FloatField()
    quantidade_horas = models.IntegerField()
    valor_total = models.FloatField()
    