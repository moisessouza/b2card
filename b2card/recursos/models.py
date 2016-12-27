from django.db import models

# Create your models here.

class Cargo (models.Model):
    nome_cargo = models.CharField(max_length=30)

class Funcionario (models.Model):
    nome = models.CharField(max_length=30)
    cargo = models.ForeignKey(Cargo, default=None, blank=True)
    cpf = models.CharField(max_length=16, default=None)
    rg = models.CharField(max_length=16, default=None)
    endereco = models.CharField(max_length=100)
    cidade = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    cep = models.CharField(max_length=10)
    salario = models.CharField(max_length=20)
    data_admissao = models.DateField(default=None, blank=True)