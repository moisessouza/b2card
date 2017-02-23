'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from faturamento.models import Parcela, Medicao, ParcelaFase, PacoteItens
from cadastros.serializers import ValorHoraSerializer
from demandas.serializers import OrcamentoFaseSerializer, DemandaSerializer

class PacoteItensSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacoteItens
        fields = ('id', 'data_criacao', 'valor_total', 'total_horas')

class ParcelaSerializer(serializers.ModelSerializer):
    demanda = DemandaSerializer()
    pacote_itens = PacoteItensSerializer()
    class Meta:
        model = Parcela
        fields = ('id', 'descricao', 'valor_parcela', 'status', 'data_previsto_parcela', 'demanda', 'pacote_itens')
        
class MedicaoSerializer(serializers.ModelSerializer):
    valor_hora = ValorHoraSerializer()
    class Meta:
        model = Medicao
        fields = ('id', 'valor_hora', 'quantidade_horas', 'valor_total')
        
class ParcelaFaseSerializer(serializers.ModelSerializer):
    parcela = ParcelaSerializer()
    fase = OrcamentoFaseSerializer()
    class Meta:
        model = ParcelaFase
        fields = ('id', 'parcela', 'fase', 'valor')