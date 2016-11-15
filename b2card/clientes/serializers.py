'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from .models import Cliente, TipoValorHora
from clientes.models import CentroResultado
        
class ClienteMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'razao_social')
        
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Cliente
        fields = ('id', 'razao_social','cnpj','endereco','cidade','estado','cep','data_contratacao','data_rescisao')
        
class TipoValorHoraSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoValorHora
        fields = ('id', 'tipo_hora', 'valor_hora')
        
class CentroResultadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CentroResultado
        fields = ('id', 'razao_social', 'cnpj')