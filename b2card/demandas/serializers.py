'''
Created on 14 de set de 2016

@author: moi09
'''
from rest_framework import serializers
from demandas.models import  Demanda, Proposta, Observacao, Ocorrencia,\
    Orcamento, Fase, ItemFase, Atividade, OrcamentoFase,\
    OrcamentoAtividade, PerfilAtividade, AtividadeProfissional,\
    FaseAtividade, AlocacaoHoras, Despesa
from cadastros.serializers import CentroCustoSerializer, ValorHoraSerializer, CentroResultadoSerializer,\
    UnidadeAdministrativaSerializer, FaseSerializer, NaturezaDemandaSerializer,\
    TipoAlocacaoSerializer
from cadastros.serializers_pessoa import PessoaFisicaComPessoaSerializer,\
    PessoaJuridicaComPessoaSerializer

class DemandaInicialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demanda
        fields = ('id', 'nome_demanda', 'status_demanda','codigo_demanda', 'percentual_concluido', 'percentual_calculado', 'data_inicio', 'data_fim')
    
class DemandaSerializer (serializers.ModelSerializer):
    cliente = PessoaJuridicaComPessoaSerializer()
    unidade_administrativa = UnidadeAdministrativaSerializer()
    responsavel = PessoaFisicaComPessoaSerializer()
    natureza_demanda = NaturezaDemandaSerializer()
    class Meta:
        model = Demanda
        fields = ('id', 'cliente','nome_demanda','descricao','status_demanda','codigo_demanda', 'unidade_administrativa', 'responsavel', 'tipo_demanda', 'responsavel_cliente', 
                  'natureza_demanda', 'percentual_concluido', 'percentual_calculado', 'data_inicio', 'data_fim', 'data_criacao', 'data_finalizacao',
                  'recorrente', 'forma_pagamento', 'particularidade_proposta')
        
class PropostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposta
        fields = ('id', 'data_recimento_solicitacao', 'data_limite_entrega', 'data_real_entrega', 'numerdo_proposta', 'data_aprovacao', 'empresa_ganhadora', 'total_horas_ganhadora')
        
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
    valor_hora_orcamento = ValorHoraSerializer()
    class Meta:
        model = Orcamento
        fields = ('id', 'total_orcamento', 'margem_risco', 'lucro_desejado', 
                  'imposto_devidos', 'total_despesas', 'valor_hora_orcamento', 
                  'valor_desejado', 'lucro_calculado_desejado', 'horas_desejado', 
                  'valor_projetado', 'horas_projetadas', 'lucro_calculado_projetado', 
                  'valor_proposto', 'horas_proposto', 'lucro_calculado_proposto')
        
class DespesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Despesa
        fields = ('id', 'descricao', 'valor', 'a_faturar')
        
class OrcamentoFaseSerializer(serializers.ModelSerializer):
    fase = FaseSerializer()
    class Meta:
        model = OrcamentoFase
        fields = ('id', 'fase', 'valor_total', 'dias')
        
class ItemFaseSerializer(serializers.ModelSerializer):
    valor_hora = ValorHoraSerializer()
    class Meta:
        model = ItemFase
        fields = ('id', 'valor_hora', 'valor_selecionado', 'quantidade_horas', 'valor_total')

class AtividadeProfissionalInicialSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtividadeProfissional
        fields = ('id', 'quantidade_horas', 'horas_alocadas_milisegundos', 'percentual_concluido', 'percentual_calculado')

class AtividadeProfissionalSerializer(serializers.ModelSerializer):
    pessoa_fisica = PessoaFisicaComPessoaSerializer()
    class Meta:
        model = AtividadeProfissional
        fields = ('id', 'pessoa_fisica', 'quantidade_horas', 'horas_alocadas_milisegundos', 'percentual_concluido', 'percentual_calculado')
        
class AlocacaoHorasSerializer(serializers.ModelSerializer):
    tipo_alocacao = TipoAlocacaoSerializer()
    class Meta:
        model = AlocacaoHoras
        fields = ('id', 'horas_alocadas_milisegundos', 'percentual_concluido', 'observacao', 'data_alocacao', 'tipo_alocacao',
                  'hora_inicio', 'hora_fim', 'data_alocacao', 'atividade_profissional')
        
class OrcamentoAtividadeSerializer(serializers.ModelSerializer):
    fase = FaseSerializer()
    class Meta:
        model = OrcamentoAtividade
        fields = ('id', 'fase', 'descricao', 'total_horas')

class PerfilAtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilAtividade
        fields = ('id', 'perfil', 'horas')

class FaseAtividadeInicialSerializer(serializers.ModelSerializer):
    fase = FaseSerializer()
    class Meta:
        model = FaseAtividade
        fields = ('id', 'fase', 'data_inicio', 'data_fim', 'percentual_concluido', 'percentual_calculado')
        
class FaseAtividadeSerializer(serializers.ModelSerializer):
    fase = FaseSerializer()
    responsavel = PessoaFisicaComPessoaSerializer()
    class Meta:
        model = FaseAtividade
        fields = ('id', 'fase', 'responsavel', 'data_inicio', 'data_fim', 'percentual_concluido', 'percentual_calculado')
        
class DemandaRelatorioSerializar(serializers.ModelSerializer):
    cliente = PessoaJuridicaComPessoaSerializer()
    class Meta:
        model = Demanda
        fields = ('id', 'nome_demanda','cliente', 'status_demanda','codigo_demanda', 'percentual_concluido', 'percentual_calculado', 'data_inicio', 'data_fim')
        
class FaseAtividadeComDemandaSerializer(serializers.ModelSerializer):
    demanda = DemandaRelatorioSerializar()
    class Meta:
        model = FaseAtividade
        fields = ('id', 'demanda')
        
class AtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Atividade
        fields = ('id', 'descricao', 'data_inicio', 'data_fim', 'percentual_concluido', 'percentual_calculado', 'data_conclusao_atividade')
        
class AtividadeComFaseAtividadeSerializer(serializers.ModelSerializer):
    fase_atividade = FaseAtividadeComDemandaSerializer()
    class Meta:
        model = Atividade
        fields = ('id', 'fase_atividade', 'descricao')
        
class AtividadeProfissionalAlocacaoHorasSerializer(serializers.ModelSerializer):
    pessoa_fisica = PessoaFisicaComPessoaSerializer()
    atividade = AtividadeComFaseAtividadeSerializer()
    class Meta:
        model = AtividadeProfissional
        fields=('id', 'pessoa_fisica', 'atividade')
        
class RelatorioAlocacaoHorasSerializer(serializers.ModelSerializer):
    tipo_alocacao = TipoAlocacaoSerializer()
    atividade_profissional = AtividadeProfissionalAlocacaoHorasSerializer()
    class Meta:
        model = AlocacaoHoras
        fields = ('id', 'horas_alocadas_milisegundos', 'percentual_concluido', 'observacao', 'data_alocacao', 'data_informada', 'tipo_alocacao',
                  'hora_inicio', 'hora_fim', 'data_alocacao', 'atividade_profissional')