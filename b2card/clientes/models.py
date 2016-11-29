from django.db import models
from cadastros.models import CentroCusto

# Create your models here.

class Cliente(models.Model):
    razao_social = models.CharField(max_length=30)
    cnpj = models.CharField(max_length=19)
    endereco = models.CharField(max_length=100)
    cidade = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    cep = models.CharField(max_length=10)
    dias_faturamento = models.IntegerField(default=None)
    dias_pagamento = models.IntegerField(default=None)
    data_contratacao = models.DateField(default=None, blank=True)
    data_rescisao = models.DateField(default=None, null=True)
    centro_custo = models.ForeignKey(CentroCusto, null=True)