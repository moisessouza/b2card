from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE

from recursos.models import Cargo


# Create your models here.
class TipoHora(models.Model):
    descricao = models.CharField(max_length=30)
    
class CentroCusto(models.Model):
    nome = models.CharField(max_length=30)

class CentroResultado(models.Model):
    nome = models.CharField(max_length=30)
    
class ContaGerencial(models.Model):
    nome = models.CharField(max_length=30)
    
class NaturezaOperacao(models.Model):
    nome = models.CharField(max_length=30)
       
class ValorHora(models.Model):
    descricao = models.CharField(max_length=30)
    tipo_hora = models.ForeignKey(TipoHora, default=None)
    centro_custo = models.ForeignKey(CentroCusto, default=None)
    centro_resultado = models.ForeignKey(CentroResultado, default=None)
    conta_gerencial = models.ForeignKey(ContaGerencial, default=None)
    natureza_operacao = models.ForeignKey(NaturezaOperacao, default=None)
    
class Vigencia(models.Model):
    data_inicio = models.DateField()
    data_fim = models.DateField()
    valor = models.FloatField()
    valor_hora = models.ForeignKey(ValorHora, default=None, on_delete=CASCADE)
    
class UnidadeAdministrativa(models.Model):
    codigo = models.CharField(max_length=10, default=None)
    nome = models.CharField(max_length=30, default=None)
    margem_risco = models.FloatField(default = None, null = True)
    imposto_devidos = models.FloatField(default = None, null = True)
    lucro_desejado = models.FloatField(default = None, null = True)
    custo_operacao_hora = models.FloatField(default = None, null = True)
    

TIPO = (
    ('C', 'CLIENTE'),
    ('F', 'FORNECEDOR'),
    ('A','AMBOS')
)

TIPO_PESSOA = (
    ('F', 'FISICA'),
    ('J', 'JURIDICA')
)

STATUS_PESSOA = (
    ('A', 'ATIVO'),
    ('I', 'INATIVO')
)

class Pessoa(models.Model):
    nome_razao_social = models.CharField(max_length=30)
    tipo = models.CharField(choices=TIPO, max_length=1)
    tipo_pessoa = models.CharField(choices=TIPO_PESSOA, max_length=1)
    data_renegociacao_valor = models.DateField(null=True, default=None)
    dias_faturamento = models.IntegerField(null=True, default=None)
    dias_pagamento = models.IntegerField(null=True, default=None)
    status = models.CharField(max_length=1, null=True, default=None)
    
ESTADO_CIVIL = (
    ('C', 'CASADO'),
    ('S', 'SOLTEIRO'),
    ('D', 'DIVORCIADO')
)    

SEXO = (
    ('M', 'MASCULINO'),
    ('F', 'FEMININO')
)    

GRAU_INSTRUCAO = (
    ('1G', '1GRAU'),
    ('2G', '2GRAU'),
    ('GR', 'GRADUADO'),
    ('PO', 'POS-GRADUADO'),
    ('DO', 'DOUTURADO'),
    ('ME', 'MESTRADO')
)

DEFICIENCIA = (
    ('N', 'NAO'),
    ('F', 'FISICA'),
    ('A', 'AUDITIVA'),
    ('V', 'VISUAL'),
    ('I', 'INTELECTUAL'),
    ('M', 'MENTAL'),
    ('R', 'REABILITADO')
)

class PessoaFisica(models.Model):
    pessoa = models.ForeignKey(Pessoa, default = None)
    cpf = models.CharField(max_length=16, default=None)
    rg = models.CharField(max_length=16, default=None)
    orgao_emissor = models.CharField(max_length=6)
    data_expedicao = models.DateField()
    email = models.CharField(max_length=50, default = None, null = True)
    data_nascimento = models.DateField()
    estado_civil = models.CharField(max_length=1, choices=ESTADO_CIVIL, default = None)
    naturalidade = models.CharField(max_length=30, default = None)
    nacionalidade = models.CharField(max_length=30, default=None)
    sexo = models.CharField(max_length=1, choices=SEXO)
    grau_instrucao = models.CharField(max_length=2, choices = GRAU_INSTRUCAO, default = None)
    nome_pai = models.CharField(max_length = 30, default = None, null = True)
    nome_mae = models.CharField(max_length = 30, default = None)
    deficiencia = models.CharField(max_length=1, choices= DEFICIENCIA, default = None, null=True)
    num_pis = models.CharField(max_length=14, default= None)
    data_emicao_pis = models.DateField()
    num_titulo_eleitoral = models.CharField(max_length=30, default=None)
    zona = models.CharField(max_length=4, default = None)
    secao = models.CharField(max_length=4, default=None)
    doc_militar = models.CharField(max_length = 30, default = None)
    categoria_doc_militar = models.CharField(max_length = 10, default = None)
    unidade_administrativas = models.ManyToManyField(UnidadeAdministrativa, default = None)
    
class PessoaJuridica(models.Model):
    pessoa = models.ForeignKey(Pessoa, default = None)
    cnpj = models.CharField(max_length=19, default = None)
    nome_fantasia = models.CharField(max_length=30, default = None, null=True)
    inscricao_estadual = models.CharField(max_length=20, default = None, null=True)
    inscricao_municipal = models.CharField(max_length=20, default = None, null=True)
    
TIPO_ENDERECO = (
    ('RE', 'RESIDENCIAL'),
    ('CO', 'COMERCIAL'),
    ('CB', 'COBRANCA'),
    ('EN', 'ENTREGA')
)

class EnderecoPessoa(models.Model):
    pessoa = models.ForeignKey(Pessoa, default = None)
    tipo = models.CharField(max_length = 2, choices = TIPO_ENDERECO, default = None)
    logradouro = models.CharField(max_length = 20)
    numero = models.CharField(max_length = 10)
    complemento = models.CharField(max_length = 30)
    bairro = models.CharField(max_length = 30, null=True, default=None)
    cidade = models.CharField(max_length = 30)
    estado = models.CharField(max_length = 20)
    cep = models.CharField(max_length = 10)
    
TIPO_TELEFONE = (
    ('R', 'RESIDENCIAL'),
    ('C', 'COMERCIAL'),
    ('M', 'CELULAR')
)

class TelefonePessoa(models.Model):
    pessoa = models.ForeignKey(Pessoa, default = None)
    tipo = models.CharField(max_length = 1, choices = TIPO_TELEFONE, default = None)
    numero = models.CharField(max_length = 20)
    
class Contato (models.Model):
    pessoa_juridica = models.ForeignKey(PessoaJuridica, default = None)
    nome = models.CharField(max_length = 30, default = None)
    email = models.CharField(max_length = 50, default = None, null = True)
    
class TelefoneContato(models.Model):
    contato = models.ForeignKey(Contato, default = None)
    tipo = models.CharField(max_length = 1, choices = TIPO_TELEFONE, default = None)
    numero = models.CharField(max_length = 20)
    
TIPO_CONTA = (
    ('S', 'CONTA SALARIO'),
    ('C', 'CONTA CORRENTE'),
    ('P', 'CONTA POUPANCA')
)

class DadosBancariosPessoa(models.Model):
    pessoa = models.ForeignKey(Pessoa, default = None)
    tipo_conta = models.CharField(max_length = 1, choices = TIPO_CONTA, default = None)
    nome_banco = models.CharField(max_length = 20, default = None)
    cod_banco = models.CharField(max_length = 4)
    cod_agencia = models.CharField(max_length = 10, default = None)
    num_conta = models.CharField(max_length = 10, default = None)
    
TIPO_PRESTADOR = (
    ('S', 'SOCIO'),
    ('A', 'AUTONOMO'),
    ('F', 'FUNCIONARIO'),
    ('P', 'PJ')
)

class Prestador(models.Model):
    pessoa_fisica = models.ForeignKey(PessoaFisica, default = None)
    tipo_prestador = models.CharField(max_length = 1, choices = TIPO_PRESTADOR)
    cargo = models.ForeignKey(Cargo, default = None, null=True)
    data_inicio = models.DateField(default = None)
    data_fim = models.DateField(default = None, null=True)
    data_contratacao = models.DateField(default = None, null = True)
    data_rescisao = models.DateField(default = None, null = True)
    data_fim_aditivo = models.DateField(default = None, null = True)
    data_exame_admissional = models.DateField(default = None, null=True)
    data_exame_demissional = models.DateField(null = True, default = None)
    data_ultimo_exame_periodico = models.DateField(null = True, default = None)
    data_ultima_avaliacao = models.DateField(null = True, default = None)
    data_proxima_avaliacao = models.DateField(null = True, default = None)
    dados_complementares = models.TextField(null = True, default = None)
    usuario = models.ForeignKey(User, default = None, null = True)
    pessoa_juridica = models.ForeignKey(PessoaJuridica, default = None, null = True)
    
class Apropriacao(models.Model):
    pessoa = models.ForeignKey(Pessoa, default = None)
    unidade_administrativa = models.ForeignKey(UnidadeAdministrativa, default = None, null = True)
    centro_custo = models.ForeignKey(CentroCusto, default = None, null = True)
    centro_resultado = models.ForeignKey(CentroResultado, default = None, null = True)
    conta_gerencial = models.ForeignKey(ContaGerencial, default = None, null = True)
    natureza_operacao = models.ForeignKey(NaturezaOperacao, default = None, null = True)
    
class CustoPrestador(models.Model):
    pessoa_fisica = models.ForeignKey(PessoaFisica, default = None)
    data_inicio = models.DateField(default = None)
    data_fim = models.DateField(default = None, null = True)
    valor = models.FloatField(max_length=30, default = None)
    
class Fase(models.Model):
    centro_resultado = models.ForeignKey(CentroResultado, default = None, null = True)
    descricao = models.CharField(max_length = 100, default = None)
    
class NaturezaDemanda(models.Model):
    descricao = models.CharField(max_length=100)
    
class TipoAlocacao(models.Model):
    descricao = models.CharField(max_length=100)