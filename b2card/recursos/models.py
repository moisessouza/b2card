from django.db import models

# Create your models here.

class Funcionario (models.Model):
    nome = models.CharField(max_length=30)
    endereco = models.CharField(max_length=100)
    cidade = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    cep = models.CharField(max_length=10)
    salario = models.FloatField(max_length=10)
    