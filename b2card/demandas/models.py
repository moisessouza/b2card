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

class Demanda(models.Model):
    cliente = models.ForeignKey(Cliente, blank=False)
    data_aprovacao = models.DateField()
    identificacao = models.CharField(max_length=30)
    numero_proposta = models.CharField(max_length=30)
    descricao = models.TextField()
    
class FaturamentoDemanda(models.Model):
    descricao = models.CharField(max_length = 30)
    data = models.DateField()
    tipo_horas = models.ForeignKey(TipoValorHora, null=True)
    valor_hora = models.CharField(max_length=10)
    quantidade_horas = models.IntegerField()
    valor_faturamento = models.CharField(max_length=10)
    status = models.CharField(max_length=1, choices=STATUS)
    data_envio_aprovacao = models.DateField()
    data_aprovacao_fatura = models.DateField()
    data_fatura = models.DateField()
    demanda = models.ForeignKey(Demanda, null=True)