from django.db import models
from recursos.models import Funcionario
from clientes.models import Cliente

# Create your models here.
class Demanda(models.Model):
    cliente = models.ForeignKey(Cliente, blank=False)
    identificacao_cliente = models.CharField(max_length=30)
    descricao_cliente = models.CharField(max_length=30)
    numero_demanda = models.CharField(max_length=30)
    coordenador = models.ForeignKey(Funcionario, blank=False)
    nomde_documento_resumido = models.CharField(max_length=30)

class Orcamento(models.Model):
    data_orcamento = models.DateField()
    unidade_administrativa = models.CharField(max_length=30)
    centro_custo = models.CharField(max_length=30)
    centro_resultado = models.CharField(max_length=30)

class Propostas(models.Model):
    numero_proposta = models.CharField(max_length=30)
    eh_corrente = models.BooleanField()
    demanda = models.ForeignKey(Demanda, blank = False)
    