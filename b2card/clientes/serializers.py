'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from .models import Cliente
        
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ('id', 'razao_social')