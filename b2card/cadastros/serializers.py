'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from cadastros.models import TipoHora, CentroCusto, ContaGerencial
        
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