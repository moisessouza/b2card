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

