from django.db import models
from django.contrib.auth.models import Group

# Create your models here.
class GrupoURL(models.Model):
    grupo = models.ForeignKey(Group, default = None)
    url = models.CharField(max_length=100, default = None)