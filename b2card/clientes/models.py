from django.db import models

# Create your models here.

class Cliente(models.Model):
    razao_social = models.CharField(max_length=30)
    cnpj = models.CharField(max_length=19)
    endereco = models.CharField(max_length=100)
    cidade = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    cep = models.CharField(max_length=10)
    data_contratacao = models.DateField(default=None, blank=True)
    data_rescisao = models.DateField(default=None, null=True)
    
class TipoValorHora(models.Model):
    cliente = models.ForeignKey(Cliente, default=None, blank=True)
    tipo_hora = models.CharField(max_length=30);
    valor_hora = models.CharField(max_length=10);
    
class CentroResultado(models.Model):
    razao_social = models.CharField(max_length=30)
    cnpj = models.CharField(max_length=19)
    cliente = models.ForeignKey(Cliente, default=None, blank=True)