'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from faturamento.models import Parcela, Medicao, ParcelaFase, LoteFaturamento
from cadastros.serializers import ValorHoraSerializer
from demandas.serializers import OrcamentoFaseSerializer, DemandaSerializer

class LoteFaturamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoteFaturamento
        fields = ('id', 'data_criacao', 'valor_total', 'total_horas')

class ParcelaSerializer(serializers.ModelSerializer):
    demanda = DemandaSerializer()
    lote_faturamento = LoteFaturamentoSerializer()
    class Meta:
        model = Parcela
        fields = ('id', 'descricao', 'valor_parcela', 'status', 'data_previsto_parcela', 'demanda', 'lote_faturamento')
        
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