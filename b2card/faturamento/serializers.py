'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from faturamento.models import Parcela

class ParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcela
        fields = ('id', 'descricao', 'valor_parcela', 'numero_horas', 'status', 'data_previsto_parcela')