'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from demandas.models import Demanda, Proposta, Tarefa, Observacao, Ocorrencia,\
    Orcamento, Fase, ItemFase, Atividade, OrcamentoFase,\
    OrcamentoAtividade, PerfilAtividade, AtividadeProfissional,\
    FaseAtividade
from cadastros.serializers import CentroCustoSerializer, ValorHoraSerializer, CentroResultadoSerializer,\
    UnidadeAdministrativaSerializer, FaseSerializer
from cadastros.serializers_pessoa import PessoaFisicaComPessoaSerializer,\
    PessoaJuridicaComPessoaSerializer
    
class DemandaSerializer (serializers.ModelSerializer):
    cliente = PessoaJuridicaComPessoaSerializer()
    unidade_administrativa = UnidadeAdministrativaSerializer()
    class Meta:
        model = Demanda
        fields = ('id', 'cliente','nome_demanda','descricao','status_demanda','codigo_demanda', 'unidade_administrativa')
        
class PropostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposta
        fields = ('id', 'data_recimento_solicitacao', 'data_limite_entrega', 'data_real_entrega', 'numerdo_proposta', 'data_aprovacao', 'empresa_ganhadora', 'total_horas_ganhadora')
        
class TarefasSerializer(serializers.ModelSerializer):
    analista_tecnico_responsavel = PessoaFisicaComPessoaSerializer()
    responsavel = PessoaFisicaComPessoaSerializer()
    class Meta:
        model = Tarefa
        fields = ('id', 'descricao','analista_tecnico_responsavel','responsavel','analise_inicio','analise_fim','analise_fim_real','densenvolvimento_inicio','desenvolvimento_fim','desenvolvimento_fim_real','homologacao_possui_sit','homologacao_inicio','homologacao_fim','homologacao_fim_real','forecast','aceite','evidencias','implantacao_producao','implantacao_in_loco')
        
class ObservacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Observacao
        fields = ('id','observacao', 'data_observacao')
        
class OcorrenciaSerializer(serializers.ModelSerializer):
    responsavel = PessoaFisicaComPessoaSerializer()
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

class AtividadeProfissionalSerializer(serializers.ModelSerializer):
    pessoa_fisica = PessoaFisicaComPessoaSerializer()
    class Meta:
        model = AtividadeProfissional
        fields = ('id', 'pessoa_fisica', 'quantidade_horas')

class OrcamentoAtividadeSerializer(serializers.ModelSerializer):
    fase = FaseSerializer()
    class Meta:
        model = OrcamentoAtividade
        fields = ('id', 'fase', 'descricao', 'total_horas')

class PerfilAtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilAtividade
        fields = ('id', 'perfil', 'horas')
        
class FaseAtividadeSerializer(serializers.ModelSerializer):
    fase = FaseSerializer()
    responsavel = PessoaFisicaComPessoaSerializer()
    class Meta:
        model = FaseAtividade
        fields = ('id', 'fase', 'responsavel', 'data_inicio', 'data_fim')
        
class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = ('id', 'descricao', 'data_inicio', 'data_fim')