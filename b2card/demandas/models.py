# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from cadastros.models import CentroCusto, ValorHora, CentroResultado, UnidadeAdministrativa,\
    Fase, PessoaFisica, PessoaJuridica, NaturezaDemanda, TipoAlocacao
import faturamento
import cadastros

# Create your models here.

STATUS = (
    ('P', 'Pendente'),
    ('A', 'Aprovado'),
    ('R', 'Reprovado'),
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

TIPO_PARCELA = (
    ('P', 'Parcela'),
    ('M', 'Medição')
)

TIPO_DEMANDA=(
    ('E', 'Externo'),
    ('I', 'Interno')
)
class Demanda(models.Model):
    cliente = models.ForeignKey(PessoaJuridica, default=None)
    nome_demanda = models.CharField(max_length=30,default=None)
    descricao = models.TextField(default=None, null=True)
    status_demanda = models.CharField(max_length=1, choices=STATUS_DEMANDA, null=True)
    codigo_demanda = models.CharField(max_length=12, null=True)
    unidade_administrativa = models.ForeignKey(UnidadeAdministrativa, default=None, null=True)
    analista_tecnico_responsavel = models.ForeignKey(PessoaFisica, null=True, related_name="%(app_label)s_%(class)s_related", related_query_name="%(app_label)s_%(class)ss")
    responsavel = models.ForeignKey(PessoaFisica, null = True)
    tipo_demanda = models.CharField(max_length=1, choices=TIPO_DEMANDA, default = None, null=True)
    natureza_demanda = models.ForeignKey(NaturezaDemanda, default = None, null = True)
    responsavel_cliente = models.CharField(max_length=30, default = None, null = True)
    data_criacao = models.DateField(default=None)
    data_inicio = models.DateField(default=None, null=True)
    data_fim = models.DateField(default=None, null=True)
    percentual_calculado = models.IntegerField(default = None, null = True)
    percentual_concluido = models.IntegerField(default = None, null = True)

class FaseAtividade(models.Model):
    demanda = models.ForeignKey(Demanda, default = None)
    fase = models.ForeignKey(Fase, default = None)
    responsavel = models.ForeignKey(PessoaFisica, default = None, null=True)
    data_inicio = models.DateField(default=None)
    data_fim = models.DateField(default=None)
    percentual_calculado = models.IntegerField(default = None, null = True)
    percentual_concluido = models.IntegerField(default = None, null = True)

class Atividade(models.Model):
    fase_atividade = models.ForeignKey(FaseAtividade, default = None)
    descricao = models.CharField(max_length=100, default = None)
    data_inicio = models.DateField(default = None)
    data_fim = models.DateField(default = None)
    percentual_calculado = models.IntegerField(default = None, null = True)
    percentual_concluido = models.IntegerField(default = None, null = True)
    
class AtividadeProfissional(models.Model):
    atividade = models.ForeignKey(Atividade, default = None)
    pessoa_fisica = models.ForeignKey(PessoaFisica, default = None)
    quantidade_horas = models.IntegerField(default = None);
    horas_alocadas_milisegundos = models.BigIntegerField(default = None, null = True)
    percentual_calculado = models.IntegerField(default = None, null = True)
    percentual_concluido = models.IntegerField(default = None, null = True)
    
class AlocacaoHoras(models.Model):
    atividade_profissional = models.ForeignKey(AtividadeProfissional, default = None, on_delete=models.PROTECT)
    hora_inicio = models.CharField(max_length=5, default = None)
    hora_fim = models.CharField(max_length=5, default = None)
    horas_alocadas_milisegundos = models.IntegerField(default=None)
    percentual_concluido = models.IntegerField()
    observacao = models.TextField(default = None, null = True)
    data_informada = models.DateField(default = None)
    data_alocacao = models.DateField(default = None)
    tipo_alocacao = models.ForeignKey(TipoAlocacao, default = None, null = True)

class Proposta(models.Model):
    data_recimento_solicitacao = models.DateField()
    data_limite_entrega = models.DateField(null=True)
    data_real_entrega = models.DateField(null=True)
    numerdo_proposta = models.CharField(max_length = 30, null=True)
    data_aprovacao = models.DateField(null=True)
    empresa_ganhadora = models.CharField(max_length = 30, null=True)
    total_horas_ganhadora = models.IntegerField(null=True)
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
    responsavel = models.ForeignKey(PessoaFisica, null=True)
    descricao_motivo = models.TextField()
    observacao = models.TextField()
    demanda = models.ForeignKey(Demanda, null=True)
    
class Orcamento(models.Model):
    demanda = models.ForeignKey(Demanda)
    valor_hora_orcamento = models.ForeignKey(ValorHora, default = None, null = True)
    descricao = models.TextField(null=True, default = None)
    total_orcamento = models.FloatField(default = None, null = True)
    margem_risco = models.FloatField(default = None, null = True)
    lucro_desejado = models.FloatField(default = None, null = True)
    imposto_devidos = models.FloatField(default = None, null = True)
    total_despesas = models.FloatField(default = None, null = True)
    
class Despesa(models.Model):
    orcamento = models.ForeignKey(Orcamento, default = None)
    descricao = models.CharField(max_length = 200, default = None)
    valor = models.FloatField(default = None)
    a_faturar = models.NullBooleanField(default = None)
    
class OrcamentoFase(models.Model):
    orcamento = models.ForeignKey(Orcamento, default=None)
    descricao = models.CharField(max_length=100)
    valor_total = models.FloatField(default = None)
    
class ItemFase(models.Model):
    fase = models.ForeignKey(OrcamentoFase, default = None)
    valor_hora = models.ForeignKey(ValorHora, default=None)
    valor_selecionado = models.FloatField()
    quantidade_horas = models.IntegerField()
    valor_total = models.FloatField()
    
class OrcamentoAtividade(models.Model):
    fase = models.ForeignKey(Fase)
    orcamento = models.ForeignKey(Orcamento, default = None)
    descricao = models.CharField(max_length=100, default = None)
    total_horas = models.IntegerField(null=True, default = None)
    
class PerfilAtividade(models.Model):
    orcamento_atividade = models.ForeignKey(OrcamentoAtividade, default = None)
    perfil = models.ForeignKey(ValorHora, default = None)
    horas = models.IntegerField(null=True, default = None)