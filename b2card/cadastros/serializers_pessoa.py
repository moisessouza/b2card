from rest_framework import serializers
from cadastros.models import Pessoa, EnderecoPessoa, TelefonePessoa,\
    DadosBancariosPessoa, PessoaFisica, Prestador, PessoaJuridica
from cadastros.serializers import CentroCustoSerializer
from django.contrib.auth.models import User

class PessoaSerializer(serializers.ModelSerializer):
    centro_custo = CentroCustoSerializer()
    class Meta:
        model=Pessoa
        fields = ('id', 'nome_razao_social', 'tipo', 'tipo_pessoa', 'centro_custo', 'data_contratacao', 'data_rescisao',
                   'data_fim_aditivo', 'data_renegociacao_valor', 'dias_faturamento', 'dias_pagamento', 'status')

class EnderecoPessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnderecoPessoa
        fields = ('id', 'tipo', 'logradouro', 'numero', 'complemento', 'cidade', 'estado', 'cep')
        
class TelefonePessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelefonePessoa
        fields = ('id', 'tipo', 'numero')
    
class DadosBancariosPessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosBancariosPessoa
        fields = ('id', 'tipo_conta', 'nome_banco', 'cod_banco', 'cod_agencia', 'num_conta')
  
class PessoaFisicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PessoaFisica
        fields = ('id', 'cpf', 'rg', 'orgao_emissor', 'data_expedicao', 'email', 'data_nascimento', 'estado_civil', 'naturalidade', 'nacionalidade', 'sexo',
                  'grau_instrucao', 'nome_pai', 'nome_mae', 'deficiencia', 'num_pis', 'data_emicao_pis', 'num_titulo_eleitoral', 'zona', 'secao', 'doc_militar', 'categoria_doc_militar')

class PessoaJuridicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PessoaJuridica
        fields = ('id', 'cnpj', 'nome_fantasia', 'inscricao_estadual', 'inscricao_municipal')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id')
        
class PrestadorSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    class Meta:
        model = Prestador
        fields = ('id', 'tipo_prestador', 'cargo', 'data_exame_admissional', 'data_exame_demissional', 'data_ultimo_exame_periodico', 'data_ultima_avaliacao', 
                  'data_proxima_avaliacao', 'dados_complementares', 'usuario')