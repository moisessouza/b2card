'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from demandas.models import Demanda, FaturamentoDemanda, Proposta
from clientes.serializers import ClienteSerializer, TipoValorHoraSerializer
     
     
     
        
class DemandaSerializer (serializers.ModelSerializer):
    cliente = ClienteSerializer()
    class Meta:
        model = Demanda
        fields = ('id', 'titulo','cliente','identificacao','descricao','tipo_demanda','status_demanda','codigo_cri')
        
class FaturamentoDemandaSerializer(serializers.ModelSerializer):
    tipo_hora = TipoValorHoraSerializer()
    class Meta:
        model = FaturamentoDemanda
        fields = ('id', 'descricao', 'data', 'tipo_hora', 'valor_hora', 'quantidade_horas', 'valor_faturamento', 'status', 'data_envio_aprovacao', 'data_aprovacao_fatura', 'data_fatura')
        
class PropostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposta
        fields = ('id', 'data_recimento_solicitacao', 'data_limite_entrega', 'data_real_entrega', 'numerdo_proposta', 'data_aprovacao', 'empresa_ganhadora', 'total_horas_ganhadora')