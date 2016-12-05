'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from faturamento.models import Parcela, Medicao
from cadastros.serializers import ValorHoraSerializer

class ParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcela
        fields = ('id', 'descricao', 'valor_parcela', 'numero_horas', 'status', 'data_previsto_parcela', 'tipo_parcela')
        
class MedicaoSerializer(serializers.ModelSerializer):
    valor_hora = ValorHoraSerializer()
    class Meta:
        model = Medicao
        fields = ('id', 'valor_hora', 'valor', 'quantidade_horas', 'valor_total')