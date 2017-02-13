from datetime import datetime
import locale
from demandas.models import Demanda, Proposta, Observacao, Ocorrencia, Orcamento,\
    FaseAtividade, Atividade, AtividadeProfissional, OrcamentoFase, ItemFase,\
    OrcamentoAtividade, PerfilAtividade, Despesa
from faturamento.models import Parcela, ParcelaFase, Medicao
from demandas.serializers import DemandaSerializer, PropostaSerializer,\
    ObservacaoSerializer, OcorrenciaSerializer, FaseAtividadeSerializer,\
    AtividadeSerializer, AtividadeProfissionalSerializer, OrcamentoSerializer,\
    ItemFaseSerializer, OrcamentoFaseSerializer, OrcamentoAtividadeSerializer,\
    DespesaSerializer
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
            if 'T' in data_string:
                data_string = data_string[:data_string.index('T')]
            data = datetime.strptime(data_string, '%Y-%m-%d')
            return data.date()
        
    return None

def serializar_data(data_string):
    d = converter_string_para_data(data_string)
    return formatar_data(d)

def converter_data_url(data_string):
    if data_string is not None and data_string != '':
        data = datetime.strptime(data_string, '%d%m%Y')
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
    
    data['data_criacao'] = formatar_data(demanda.data_criacao)
    
    propostas_list = PropostaSerializer(propostas, many=True).data
    for i in propostas_list:
        if 'data_recimento_solicitacao' in i:
            i['data_recimento_solicitacao'] = serializar_data(i['data_recimento_solicitacao'])
        if 'data_limite_entrega' in i:
            i['data_limite_entrega'] = serializar_data(i['data_limite_entrega'])
        if 'data_real_entrega' in i:
            i['data_real_entrega'] = serializar_data(i['data_real_entrega'])
        if 'data_aprovacao' in i:
            i['data_aprovacao'] = serializar_data(i['data_aprovacao'])
    
    observacoes_list = ObservacaoSerializer(observacoes, many=True).data
    for i in observacoes_list:
        if 'data_observacao' in i:
            i['data_observacao'] = serializar_data(i['data_observacao'])
        
    ocorrencias_list = OcorrenciaSerializer(ocorrencias, many=True).data
    for i in ocorrencias:
        if 'data_solicitacao' in i:
            i['data_solicitacao'] = serializar_data(i['data_solicitacao'])
        if 'data_prevista_conclusao' in i:
            i['data_prevista_conclusao'] = serializar_data(i['data_prevista_conclusao'])
        
    orcamento_dict = serializar_orcamento(orcamentos)
    
    fase_atividade_list = serializar_fase_atividade(fase_atividades)
        
    parcelas_list = ParcelaSerializer(parcelas, many=True).data
    for i in parcelas_list:
        
        i['data_previsto_parcela'] = serializar_data(i['data_previsto_parcela'])
        
        parcelafase_list = ParcelaFase.objects.filter(parcela = i['id'])
        parcelafaseserializer_list = ParcelaFaseSerializer(parcelafase_list, many=True).data
        
        for pf in parcelafaseserializer_list:
            medicoes = Medicao.objects.filter(parcela_fase__id = pf['id'])
            medicao_list = MedicaoSerializer(medicoes, many=True).data
            pf['medicoes'] = medicao_list
        i['parcelafases'] = parcelafaseserializer_list

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
            orcamento_fases = OrcamentoFase.objects.filter(orcamento = orcamento)
            
            fases_list = OrcamentoFaseSerializer(orcamento_fases, many=True).data
            for i in fases_list:
                itens_fase = ItemFase.objects.filter(orcamento_fase__id = i['id'])
                intes_fase_list = ItemFaseSerializer(itens_fase, many=True).data
                i['itensfase'] = intes_fase_list
                
            orcamento_dict['orcamento_fases'] = fases_list
            
            orcamento_atividades = OrcamentoAtividade.objects.filter(orcamento = orcamento)
            orcamento_atividades_list = OrcamentoAtividadeSerializer(orcamento_atividades, many=True).data
            
            if orcamento_atividades_list:
                for o in orcamento_atividades_list:
                    perfil_atividades = PerfilAtividade.objects.filter(orcamento_atividade__id = o['id'])
                    dict = {}
                    for p in perfil_atividades:
                        dict[p.perfil.id] = { 'horas': p.horas }
                    o['colunas'] = dict

            orcamento_dict['orcamento_atividades'] = orcamento_atividades_list
            
            despesas = Despesa.objects.filter(orcamento = orcamento)
            despesa_list = DespesaSerializer(despesas, many=True).data
            
            orcamento_dict['despesas'] = despesa_list
            
        return orcamento_dict;
    
def serializar_fase_atividade(fase_atividades):
    
    if fase_atividades:
        fase_atividade_list = FaseAtividadeSerializer(fase_atividades, many = True).data   
        for i in fase_atividade_list:
            
            if 'data_inicio' in i:
                i['data_inicio'] = serializar_data(i['data_inicio'])
            if 'data_fim' in i:
                i['data_fim'] = serializar_data(i['data_fim'])
            
            atividades = Atividade.objects.filter(fase_atividade__id = i['id'])
            
            atividade_list = []
            
            if atividades:
                atividade_list = AtividadeSerializer(atividades, many=True).data
                for a in atividade_list:
                    if 'data_inicio' in a:
                        a['data_inicio'] = serializar_data(a['data_inicio'])
                    if 'data_fim' in a:
                        a['data_fim'] = serializar_data(a['data_fim'])

                    atividade_profissionais = AtividadeProfissional.objects.filter(atividade__id = a['id'])
                    
                    if atividade_profissionais:
                        a['atividadeprofissionais'] = AtividadeProfissionalSerializer(atividade_profissionais, many=True).data
                    
            i['atividades'] = atividade_list
            
    return fase_atividade_list