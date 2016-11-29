from __future__ import unicode_literals

from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class TipoHora(models.Model):
    descricao = models.CharField(max_length=30)
    
class CentroCusto(models.Model):
    nome = models.CharField(max_length=30)

class CentroResultado(models.Model):
    nome = models.CharField(max_length=30)
    
class ContaGerencial(models.Model):
    nome = models.CharField(max_length=30)
    
class NaturezaOperacao(models.Model):
    nome = models.CharField(max_length=30)
       
class ValorHora(models.Model):
    descricao = models.CharField(max_length=30)
    tipo_hora = models.ForeignKey(TipoHora, default=None)
    centro_custo = models.ForeignKey(CentroCusto, default=None)
    centro_resultado = models.ForeignKey(CentroResultado, default=None)
    conta_gerencial = models.ForeignKey(ContaGerencial, default=None)
    natureza_operacao = models.ForeignKey(NaturezaOperacao, default=None)
    
class Vigencia(models.Model):
    data_inicio = models.DateField()
    data_fim = models.DateField()
    valor = models.FloatField()
    valor_hora = models.ForeignKey(ValorHora, default=None, on_delete=CASCADE)
    
class UnidadeAdministrativa(models.Model):
    codigo = models.CharField(max_length=10, default=None)
    nome = models.CharField(max_length=30, default=None)