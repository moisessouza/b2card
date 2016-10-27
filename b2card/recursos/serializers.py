'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from .models import Funcionario
        
class FuncionarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Funcionario
        fields = ('id', 'nome')