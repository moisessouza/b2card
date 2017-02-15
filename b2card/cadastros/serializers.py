'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from cadastros.models import TipoHora, CentroCusto, ContaGerencial, NaturezaOperacao, ValorHora, Vigencia,\
    UnidadeAdministrativa, Fase, NaturezaDemanda, TipoAlocacao
        
class TipoHoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoHora
        fields = ('id', 'descricao')
        
        
class CentroCustoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroCusto
        fields = ('id', 'nome')
        
class CentroResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroCusto
        fields = ('id', 'nome')    
        
class ContaGerencialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContaGerencial
        fields = ('id', 'nome')      
        
class NaturezaOperacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = NaturezaOperacao
        fields = ('id', 'nome')
        
class ValorHoraSerializer(serializers.ModelSerializer):
    tipo_hora = TipoHoraSerializer()
    centro_custo = CentroCustoSerializer()
    centro_resultado = CentroResultadoSerializer()
    conta_gerencial = ContaGerencialSerializer()
    natureza_operacao = NaturezaOperacaoSerializer()
    class Meta:
        model = ValorHora
        fields = ('id', 'descricao', 'tipo_hora','centro_custo','centro_resultado','conta_gerencial','natureza_operacao')
        
class VigenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vigencia
        fields = ('id', 'data_inicio', 'data_fim', 'valor')
        
class UnidadeAdministrativaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeAdministrativa
        fields = ('id', 'codigo', 'nome', 'margem_risco', 'imposto_devidos', 'lucro_desejado')
        
class FaseSerializer(serializers.ModelSerializer):
    centro_resultado = CentroResultadoSerializer()
    class Meta:
        model = Fase
        fields = ('id', 'descricao', 'centro_resultado')

class TipoAlocacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAlocacao
        fields = ('id', 'descricao')
    
class NaturezaDemandaSerializer(serializers.ModelSerializer):
    class Meta:
        model = NaturezaDemanda
        fields = ('id', 'descricao')