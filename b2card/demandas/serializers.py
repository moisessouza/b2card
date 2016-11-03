'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from demandas.models import Demanda, FaturamentoDemanda
from clientes.serializers import ClienteSerializer, TipoValorHoraSerializer
        
class DemandaSerializer (serializers.ModelSerializer):
    cliente = ClienteSerializer()
    class Meta:
        model = Demanda
        fields = ('id', 'cliente', 'data_aprovacao', 'identificacao', 'numero_proposta', 'descricao')
        
class FaturamentoDemandaSerializer(serializers.ModelSerializer):
    tipo_hora = TipoValorHoraSerializer()
    class Meta:
        model = FaturamentoDemanda
        fields = ('id', 'descricao', 'data', 'tipo_hora', 'valor_hora', 'quantidade_horas', 'valor_faturamento', 'status', 'data_envio_aprovacao', 'data_aprovacao_fatura', 'data_fatura')