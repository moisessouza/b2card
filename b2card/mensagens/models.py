from django.db import models
from cadastros.models import PessoaFisica

# Create your models here.

TAG_MENSAGEM = (
    ('E', 'Exame Periodico'),
    ('A', 'Alocacao de horas'),
    ('N', 'Aniversarios'),
    ('D', 'Não lancamento dois dias')
)

class Mensagem(models.Model):
    pessoa_fisica = models.ForeignKey(PessoaFisica, default = None)
    data_criacao = models.DateField(default = None)
    origem =models.CharField(max_length=30, default="SISTEMA", null=True)
    texto = models.TextField(default = None)
    lido = models.NullBooleanField(default = False)
    tag = models.CharField(choices = TAG_MENSAGEM, max_length=1, default = None)
    
class Responsavel(models.Model):
    pessoa_fisica = models.ForeignKey(PessoaFisica, default = None)
    tag = models.CharField(choices = TAG_MENSAGEM, max_length=1, default = None)
    ativo = models.NullBooleanField(default = False)