'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from faturamento.models import Parcela, Medicao, ParcelaFase
from cadastros.serializers import ValorHoraSerializer
from demandas.serializers import FaseSerializer

class ParcelaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parcela
        fields = ('id', 'descricao', 'valor_parcela', 'numero_horas', 'status', 'data_previsto_parcela', 'tipo_parcela')
        
class MedicaoSerializer(serializers.ModelSerializer):
    valor_hora = ValorHoraSerializer()
    class Meta:
        model = Medicao
        fields = ('id', 'valor_hora', 'valor', 'quantidade_horas', 'valor_total')
        
class ParcelaFaseSerializer(serializers.ModelSerializer):
    parcela = ParcelaSerializer()
    fase = FaseSerializer()
    class Meta:
        model = ParcelaFase
        fields = ('id', 'parcela', 'fase')