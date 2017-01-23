'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from .models import Cargo
        
class CargoSerializer(serializers.ModelSerializer):
    nome_cargo = serializers.CharField(max_length=30, required=False)
    class Meta:
        model = Cargo
        fields = ('id', 'nome_cargo', 'gestor')