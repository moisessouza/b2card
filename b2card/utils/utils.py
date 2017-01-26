from datetime import datetime
import locale
from demandas.models import Demanda, Proposta, Observacao, Ocorrencia, Orcamento,\
    FaseAtividade, Atividade, AtividadeProfissional, OrcamentoFase, ItemFase,\
    OrcamentoAtividade, PerfilAtividade
from faturamento.models import Parcela, ParcelaFase, Medicao
from demandas.serializers import DemandaSerializer, PropostaSerializer,\
    ObservacaoSerializer, OcorrenciaSerializer, FaseAtividadeSerializer,\
    AtividadeSerializer, AtividadeProfissionalSerializer, OrcamentoSerializer,\
    ItemFaseSerializer, OrcamentoFaseSerializer, OrcamentoAtividadeSerializer
from faturamento.serializers import ParcelaSerializer, ParcelaFaseSerializer,\
    MedicaoSerializer
import re

def formatar_data(data):
    if data is not None:
        iso = data.isoformat()
        tokens = iso.strip()
        tokens = iso.split('-')
        return "%s/%s/%s" % (tokens[2],tokens[1],tokens[0])
    else:
        return None
    
def converter_string_para_data(data_string):
    if data_string is not None and data_string != '':
        data_padrao = re.compile('\d\d/\d\d/\d\d\d\d')
        if data_padrao.match(data_string):
            data = datetime.strptime(data_string, '%d/%m/%Y')
            return data.date()
        else:
            data_string = data_string[:data_string.index('T')]
            data = datetime.strptime(data_string, '%Y-%m-%d')
            return data.date()
        
    return None
    
def converter_string_para_float(float_string):
    if float_string is not None and float_string != '':
        float_string = float_string.replace('.', '').replace(',', '.')
        return float(float_string);
    else:
        return None

def serializarDemanda(demanda_id):
    demanda = Demanda.objects.get(pk=demanda_id)
    return serializarDemandaObject(demanda)

def serializarDemandaObject(demanda):
       
    propostas = Proposta.objects.filter(demanda__id=demanda.id)
    observacoes = Observacao.objects.filter(demanda__id=demanda.id)
    ocorrencias = Ocorrencia.objects.filter(demanda__id=demanda.id)
    orcamentos = Orcamento.objects.filter(demanda__id=demanda.id)
    fase_atividades = FaseAtividade.objects.filter(demanda__id=demanda.id)
    parcelas = Parcela.objects.filter(demanda__id=demanda.id)
    
    data = DemandaSerializer(demanda).data
    
    propostas_list = []
    for i in propostas:
        proposta = PropostaSerializer(i).data
        proposta['data_recimento_solicitacao'] = formatar_data(i.data_recimento_solicitacao)
        proposta['data_limite_entrega'] = formatar_data(i.data_limite_entrega)
        proposta['data_real_entrega'] = formatar_data(i.data_real_entrega)
        proposta['data_aprovacao'] = formatar_data(i.data_aprovacao)
        propostas_list.append(proposta)
    
    observacoes_list = []
    for i in observacoes:
        observacao = ObservacaoSerializer(i).data
        observacao['data_observacao'] = formatar_data(i.data_observacao)
        observacoes_list.append(observacao)
        
    ocorrencias_list = []
    for i in ocorrencias:
        ocorrencia = OcorrenciaSerializer(i).data
        ocorrencia['data_solicitacao'] = formatar_data(i.data_solicitacao)
        ocorrencia['data_prevista_conclusao'] = formatar_data(i.data_prevista_conclusao)
        ocorrencias_list.append(ocorrencia)
        
    orcamento_dict = serializar_orcamento(orcamentos)
    
    fase_atividade_list = serializar_fase_atividade(fase_atividades)
        
    parcelas_list = []
    for i in parcelas:
        
        parcela = ParcelaSerializer(i).data
        parcela['data_previsto_parcela'] = formatar_data(i.data_previsto_parcela)
        
        parcelafase_list = ParcelaFase.objects.filter(parcela = i)
        parcelafaseserializer_list = []
        for pf in parcelafase_list:
            parcelafaseserializer = ParcelaFaseSerializer(pf).data
            medicoes = Medicao.objects.filter(parcela_fase = pf)
            medicao_list = MedicaoSerializer(medicoes, many=True).data
            parcelafaseserializer['medicoes'] = medicao_list
            
            parcelafaseserializer_list.append(parcelafaseserializer)
        parcela['parcelafases'] = parcelafaseserializer_list
            
        parcelas_list.append(parcela)
    
    data['propostas'] = propostas_list
    data['observacoes'] = observacoes_list
    data['ocorrencias'] = ocorrencias_list
    data['orcamento'] = orcamento_dict
    data['fase_atividades'] = fase_atividade_list
    data['parcelas'] = parcelas_list
   
    return data

def serializar_orcamento(orcamentos):
        
        orcamento_dict = {}
        if  orcamentos:
            orcamento = orcamentos[0]
            orcamento_dict = OrcamentoSerializer(orcamento).data
            fases = OrcamentoFase.objects.filter(orcamento = orcamento)
            
            fases_list = []
            for i in fases:
                itens_fase = ItemFase.objects.filter(fase = i)
                intes_fase_list = ItemFaseSerializer(itens_fase, many=True).data
                fase_dict = OrcamentoFaseSerializer(i).data
                fase_dict['itensfase'] = intes_fase_list
                fases_list.append(fase_dict)
                
            orcamento_dict['fases'] = fases_list
            
            orcamento_atividades = OrcamentoAtividade.objects.filter(orcamento = orcamento)
            orcamento_atividades_list = []
            
            if orcamento_atividades:
                for o in orcamento_atividades:
                    orcamento_atividade_dict = OrcamentoAtividadeSerializer(o).data
                    perfil_atividades = PerfilAtividade.objects.filter(orcamento_atividade = o)
                    dict = {}
                    for p in perfil_atividades:
                        dict[p.perfil.id] = { 'horas': p.horas }
                    orcamento_atividade_dict['colunas'] = dict
                    orcamento_atividades_list.append(orcamento_atividade_dict)
            orcamento_dict['orcamento_atividades'] = orcamento_atividades_list
            
        return orcamento_dict;
    
def serializar_fase_atividade(fase_atividades):
    fase_atividade_list = []
    if fase_atividades:
        
        for i in fase_atividades:
            
            fase_atividade = FaseAtividadeSerializer(i).data
            fase_atividade['data_inicio'] = formatar_data(i.data_inicio)
            fase_atividade['data_fim'] = formatar_data(i.data_fim)
            
            atividades = Atividade.objects.filter(fase_atividade = i)
            
            atividade_list = []
            
            if atividades:
                for a in atividades:
                    
                    atividade = AtividadeSerializer(a).data
                    
                    atividade['data_inicio'] = formatar_data(a.data_inicio)
                    atividade['data_fim'] = formatar_data(a.data_fim)
                    
                    atividade_profissionais = AtividadeProfissional.objects.filter(atividade = a)
                    
                    if atividade_profissionais:
                        atividade['atividadeprofissionais'] = AtividadeProfissionalSerializer(atividade_profissionais, many=True).data
                
                    atividade_list.append(atividade)
                    
            fase_atividade['atividades'] = atividade_list
            fase_atividade_list.append(fase_atividade)
            
    return fase_atividade_list