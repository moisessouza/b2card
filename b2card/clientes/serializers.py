'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from .models import Cliente
        
class ClienteMinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'razao_social','dias_pagamento','dias_faturamento')
        
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Cliente
        fields = ('id', 'razao_social','cnpj','endereco','cidade','estado','cep','dias_pagamento','dias_faturamento','data_contratacao','data_rescisao')
        

