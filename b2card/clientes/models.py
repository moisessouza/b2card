from django.db import models

# Create your models here.

class Cliente(models.Model):
    
    cnpj = models.CharField(max_length=19)
    razao_social = models.CharField(max_length=30)
    endereco = models.CharField(max_length=100)
    cidade = models.CharField(max_length=20)
    estado = models.CharField(max_length=20)
    cep = models.CharField(max_length=10)