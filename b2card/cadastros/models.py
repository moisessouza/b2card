from __future__ import unicode_literals

from django.db import models

# Create your models here.
class TipoHora(models.Model):
    descricao = models.CharField(max_length=30)
