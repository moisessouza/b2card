from django.shortcuts import render
from rest_framework.decorators import api_view
from demandas.models import Atividade, Demanda, FaseAtividade,\
    AtividadeProfissional, AlocacaoHoras
from demandas.serializers import DemandaSerializer, AtividadeSerializer,\
    FaseAtividadeSerializer, AtividadeProfissionalSerializer
from rest_framework.response import Response
from cadastros.models import PessoaJuridica
from cadastros.serializers_pessoa import PessoaJuridicaSerializer,\
    PessoaJuridicaComPessoaSerializer
from utils.utils import formatar_data
import datetime

# Create your views here.
def index (request):
    return render(request, 'first_page.html')

@api_view(['GET'])
def buscar_atividades_usuario(request, format=None):

    clientes  = PessoaJuridica.objects.filter(demanda__faseatividade__atividade__atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id).distinct()

    cliente_list = [];

    for c in clientes:

        cliente_dict = PessoaJuridicaComPessoaSerializer(c).data

        demandas = Demanda.objects.filter(cliente = c, faseatividade__atividade__atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id).distinct();
        demanda_list = []
        
        for i in demandas:
    
            demanda_dict = DemandaSerializer(i).data
            demanda_list.append(demanda_dict)
            
            fase_atividade_list = []
            fase_atividades = FaseAtividade.objects.filter(demanda=i, atividade__atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id).distinct();
            
            for f in fase_atividades:
                
                fase_atividade_dict = FaseAtividadeSerializer(f).data
                fase_atividade_list.append(fase_atividade_dict)
                
                atividades = Atividade.objects.filter(fase_atividade=f,atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id)
                atividade_list = [];
                
                for a in atividades:
                    
                    atividade_dict = AtividadeSerializer(a).data
                    atividade_dict['data_inicio'] = formatar_data(a.data_inicio)
                    atividade_dict['data_fim'] = formatar_data(a.data_fim)
                    atividade_list.append(atividade_dict)
                    atividade_profissional =  AtividadeProfissional.objects.filter(atividade = a, pessoa_fisica__prestador__usuario__id=request.user.id)[:1]
                    
                    atividade_profissional_dict = AtividadeProfissionalSerializer(atividade_profissional[0]).data
                    atividade_dict['atividade_profissional'] = atividade_profissional_dict
                    
                fase_atividade_dict['atividades']=atividade_list
                    
            demanda_dict['fase_atividades']=fase_atividade_list       
        
        cliente_dict['demandas'] = demanda_list
        
        cliente_list.append(cliente_dict)
        
    return Response(cliente_list)


def alocar_horas(request, format=None):
    
    atividade_profissional = None
    if 'atividade_profissional' in request.data:
        atividade_profissional = AtividadeProfissional.objects.get(pk=request.data['atividade_profissional']['id'])
        del request.data['atividade_profissional']
    
    alocacao_horas = AlocacaoHoras(**request.data)
    alocacao_horas.atividade_profissional = atividade_profissional
    alocacao_horas.data_alocacao = datetime.datetime.now()
    alocacao_horas.save();
    
    horas_alocadas_milisegundos = request.data['horas_alocadas_milisegundos']
    percentual_concluido = request.data['percentual_concluido']    
    
    if (atividade_profissional.horas_alocadas_milisegundos):
        atividade_profissional.horas_alocadas_milisegundos += horas_alocadas_milisegundos
    else:
        atividade_profissional.horas_alocadas_milisegundos = horas_alocadas_milisegundos
        
    atividade_profissional.percentual_concluido = percentual_concluido
    atividade_profissional.save();
    
    return Response(AtividadeProfissionalSerializer(atividade_profissional).data)
    