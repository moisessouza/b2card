'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from demandas.models import Demanda, FaturamentoDemanda, Proposta, Tarefa, Observacao
from clientes.serializers import ClienteSerializer, TipoValorHoraSerializer
from recursos.serializers import FuncionarioSerializer
     
     
     
        
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
        
class TarefasSerializer(serializers.ModelSerializer):
    analista_tecnico_responsavel = FuncionarioSerializer()
    responsavel = FuncionarioSerializer()
    class Meta:
        model = Tarefa
        fields = ('id', 'descricao','analista_tecnico_responsavel','responsavel','analise_inicio','analise_fim','analise_fim_real','densenvolvimento_inicio','desenvolvimento_fim','desenvolvimento_fim_real','homologacao_possui_sit','homologacao_inicio','homologacao_fim','homologacao_fim_real','forecast','aceite','evidencias','implantacao_producao','implantacao_in_loco')
        
class ObservacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observacao
        fields = ('id','observacao', 'data_observacao')