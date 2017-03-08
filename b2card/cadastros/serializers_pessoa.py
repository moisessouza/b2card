from rest_framework import serializers
from cadastros.models import Pessoa, EnderecoPessoa, TelefonePessoa,\
    DadosBancariosPessoa, PessoaFisica, Prestador, PessoaJuridica, Contato,\
    TelefoneContato, Apropriacao, CustoPrestador, Arquivo
from cadastros.serializers import CentroCustoSerializer,\
    UnidadeAdministrativaSerializer, CentroResultadoSerializer,\
    ContaGerencialSerializer, NaturezaOperacaoSerializer
from django.contrib.auth.models import User
from recursos.serializers import CargoSerializer

class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model=Pessoa
        fields = ('id', 'nome_razao_social', 'tipo', 'tipo_pessoa', 
                  'data_renegociacao_valor', 'dias_faturamento', 'dias_pagamento', 'status')

class EnderecoPessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnderecoPessoa
        fields = ('id', 'tipo', 'logradouro', 'numero', 'complemento', 'cidade', 'estado', 'cep', 'bairro')
        
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
                  'grau_instrucao', 'nome_pai', 'nome_mae', 'deficiencia', 'num_pis', 'data_emicao_pis', 'num_titulo_eleitoral', 'zona', 'secao', 'doc_militar', 
                  'categoria_doc_militar')

class PessoaFisicaComPessoaSerializer(serializers.ModelSerializer):
    pessoa = PessoaSerializer()
    class Meta:
        model = PessoaFisica
        fields = ('id', 'cpf', 'rg', 'orgao_emissor', 'data_expedicao', 'email', 'data_nascimento', 'estado_civil', 'naturalidade', 'nacionalidade', 'sexo',
                  'grau_instrucao', 'nome_pai', 'nome_mae', 'deficiencia', 'num_pis', 'data_emicao_pis', 'num_titulo_eleitoral', 'zona', 'secao', 'doc_militar', 'categoria_doc_militar', 'pessoa')

class ArquivoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Arquivo
        fields = ('id',  'nome_arquivo', 'content_type', 'tamanho', 'path_arquivo')

class PessoaJuridicaSerializer(serializers.ModelSerializer):
    arquivo = ArquivoSerializer()
    class Meta:
        model = PessoaJuridica
        fields = ('id', 'cnpj', 'nome_fantasia', 'inscricao_estadual', 'inscricao_municipal', 'forma_pagamento', 'particularidade_proposta', 'arquivo')
                
class PessoaJuridicaComPessoaSerializer(serializers.ModelSerializer):
    pessoa = PessoaSerializer()
    class Meta:
        model = PessoaJuridica
        fields = ('id', 'cnpj', 'nome_fantasia', 'inscricao_estadual', 'inscricao_municipal', 'pessoa', 'forma_pagamento', 'particularidade_proposta')
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')
        
class PrestadorSerializer(serializers.ModelSerializer):
    usuario = UserSerializer()
    cargo = CargoSerializer()
    pessoa_juridica = PessoaJuridicaSerializer()
    class Meta:
        model = Prestador
        fields = ('id', 'tipo_prestador', 'cargo', 'data_contratacao', 'data_rescisao', 'data_fim_aditivo', 'data_exame_admissional', 'data_exame_demissional', 'data_ultimo_exame_periodico', 'data_ultima_avaliacao', 
                  'data_proxima_avaliacao', 'dados_complementares', 'usuario', 'cargo', 'pessoa_juridica')
        
class ContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contato
        fields = ('id', 'nome', 'email')
        
class TelefoneContatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelefoneContato
        fields = ('id', 'tipo', 'numero')
        
        
class ApropriacaoSerializer(serializers.ModelSerializer):
    unidade_administrativa = UnidadeAdministrativaSerializer()
    centro_custo = CentroCustoSerializer()
    centro_resultado = CentroResultadoSerializer()
    conta_gerencial = ContaGerencialSerializer()
    natureza_operacao = NaturezaOperacaoSerializer()
    class Meta:
        model = Apropriacao
        fields = ('id', 'unidade_administrativa', 'centro_custo', 'centro_resultado', 'conta_gerencial', 'natureza_operacao')
        
class CustoPrestadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustoPrestador
        fields = ('id', 'data_inicio', 'data_fim', 'valor')
        
