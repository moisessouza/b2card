'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from .models import Funcionario, Cargo
        
class CargoSerializer(serializers.ModelSerializer):
    nome_cargo = serializers.CharField(max_length=30, required=False)
    class Meta:
        model = Cargo
        fields = ('id', 'nome_cargo')
class FuncionarioSerializer(serializers.ModelSerializer):
    cargo = CargoSerializer(read_only=True)
    class Meta:
        model = Funcionario
        fields = ('id', 'nome', 'cpf', 'rg','endereco', 'cidade', 'estado', 'cep', 'salario', 'cargo')