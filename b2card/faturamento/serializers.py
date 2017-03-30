'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from faturamento.models import Parcela, Medicao, ParcelaFase, PacoteItens,\
    LoteDespesa, ItemDespesa
from cadastros.serializers import ValorHoraSerializer, TipoDespesaSerializer
from demandas.serializers import OrcamentoFaseSerializer, DemandaSerializer,\
    DemandaInicialSerializer
from cadastros.serializers_pessoa import PessoaSerializer

class PacoteItensSerializer(serializers.ModelSerializer):
    class Meta:
        model = PacoteItens
        fields = ('id', 'data_criacao', 'valor_total', 'total_horas')

class ParcelaSerializer(serializers.ModelSerializer):
    demanda = DemandaSerializer()
    pacote_itens = PacoteItensSerializer()
    class Meta:
        model = Parcela
        fields = ('id', 'descricao', 'valor_parcela', 'status', 'demanda', 'pacote_itens', 'data_previsto_parcela', 'nota_fiscal',
                  'data_envio_aprovacao', 'data_aprovacao_faturamento', 'data_previsto_pagamento', 'data_faturamento', 'data_pagamento')
        
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
        
class LoteDespesaSerializer(serializers.ModelSerializer):
    demanda = DemandaInicialSerializer()
    pessoa = PessoaSerializer()
    class Meta:
        model = LoteDespesa
        fields = ('id', 'demanda', 'pessoa', 'motivo_despesa', 'data', 'status', 'valor_total')
        
class ItemDespesaSerializer(serializers.ModelSerializer):
    tipo_despesa = TipoDespesaSerializer()
    class Meta:
        model = ItemDespesa
        fields = ('id', 'num_documento', 'valor', 'data', 'tipo_despesa', 'descricao')