from django.db import models
from recursos.models import Funcionario
from clientes.models import Cliente
from datetime import datetime  

# Create your models here.
class Demanda(models.Model):
    cliente = models.ForeignKey(Cliente, blank=False)
    identificacao_cliente = models.CharField(max_length=30)
    descricao_cliente = models.CharField(max_length=30)
    numero_demanda = models.CharField(max_length=30)
    unidade_administrativa = models.CharField(max_length=30, default=None)
    coordenador = models.ForeignKey(Funcionario, blank=False)
    nomde_documento_resumido = models.CharField(max_length=30)
    informacoes_nfe = models.TextField()
    observacoes = models.TextField()

class Orcamento(models.Model):
    centro_custo = models.CharField(max_length=30)
    centro_resultado = models.CharField(max_length=30)

class Propostas(models.Model):
    numero_proposta = models.CharField(max_length=30)
    eh_corrente = models.BooleanField()
    data_proposta = models.DateField(default=None)
    orcamento = models.ForeignKey(Orcamento, blank = False, default=None)
    demanda = models.ForeignKey(Demanda, blank = False)
    
class Atividades(models.Model):
    descricao_atividade = models.CharField(max_length=30)
    responsavel = models.ForeignKey(Funcionario, blank=False)
    tipo_atividade = models.CharField(max_length=30)
    demanda = models.ForeignKey(Demanda, blank=False)
       
class DespesasExtras(models.Model):
    descricao = models.CharField(max_length=30)
    tipo_despesa = models.CharField(max_length=30)
    valor = models.FloatField(max_length=10)