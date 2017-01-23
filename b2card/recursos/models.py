from django.db import models

# Create your models here.

class Cargo (models.Model):
    nome_cargo = models.CharField(max_length=30)
    gestor = models.BooleanField(default = False);
