'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from demandas.models import Demanda, FaturamentoDemanda, Proposta, Tarefa, Observacao, Ocorrencia,\
    Orcamento, Fase, ItemFase, Atividade, ValorHoraFaturamento, OrcamentoFase,\
    OrcamentoAtividade, PerfilAtividade
from clientes.serializers import ClienteSerializer
from recursos.serializers import FuncionarioSerializer
from cadastros.serializers import CentroCustoSerializer, ValorHoraSerializer, CentroResultadoSerializer,\
    UnidadeAdministrativaSerializer, FaseSerializer
    
class DemandaSerializer (serializers.ModelSerializer):
    cliente = ClienteSerializer()
    unidade_administrativa = UnidadeAdministrativaSerializer()
    class Meta:
        model = Demanda
        fields = ('id', 'cliente','nome_demanda','descricao','status_demanda','codigo_demanda', 'unidade_administrativa')
        
class FaturamentoDemandaSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaturamentoDemanda
        fields = ('id', 'descricao', 'numero_nota', 'valor_total_faturamento', 'status', 'data_envio_aprovacao', 'data_previsto_faturamento', 'data_previsto_pagamento', 'data_pagamento', 'data_fatura')

class ValorHoraFaturamentoSerializer(serializers.ModelSerializer):
    valor_hora = ValorHoraSerializer()
    class Meta:
        model = ValorHoraFaturamento
        fields = ('id','valor_hora', 'valor', 'quantidade_horas', 'valor_faturamento')
        
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
        
class OcorrenciaSerializer(serializers.ModelSerializer):
    responsavel = FuncionarioSerializer()
    class Meta:
        model = Ocorrencia
        fields = ('id', 'tipo_ocorrencia', 'descricao', 'nome_solicitante', 'data_solicitacao', 'data_prevista_conclusao', 'etapa', 'responsavel', 'descricao_motivo', 'observacao')
        
class OrcamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orcamento
        fields = ('id', 'total_orcamento')
        
class OrcamentoFaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrcamentoFase
        fields = ('id', 'descricao', 'valor_total')
        
class ItemFaseSerializer(serializers.ModelSerializer):
    valor_hora = ValorHoraSerializer()
    class Meta:
        model = ItemFase
        fields = ('id', 'valor_hora', 'valor_selecionado', 'quantidade_horas', 'valor_total')
        
class AtividadeSerializer(serializers.ModelSerializer):
    responsavel = FuncionarioSerializer()
    centro_resultado = CentroResultadoSerializer()
    class Meta:
        model = Atividade
        fields = ('id', 'titulo', 'responsavel', 'centro_resultado', 'horas_previstas')
        
class OrcamentoAtividadeSerializer(serializers.ModelSerializer):
    fase = FaseSerializer()
    class Meta:
        model = OrcamentoAtividade
        fields = ('id', 'fase', 'descricao', 'total_horas')

class PerfilAtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilAtividade
        fields = ('id', 'perfil', 'horas')