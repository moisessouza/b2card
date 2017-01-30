from django.shortcuts import render
from rest_framework.decorators import api_view
from demandas.models import Atividade, Demanda, FaseAtividade,\
    AtividadeProfissional, AlocacaoHoras
from demandas.serializers import DemandaSerializer, AtividadeSerializer,\
    FaseAtividadeSerializer, AtividadeProfissionalSerializer,\
    AlocacaoHorasSerializer
from rest_framework.response import Response
from cadastros.models import PessoaJuridica, TipoAlocacao
from cadastros.serializers_pessoa import PessoaJuridicaSerializer,\
    PessoaJuridicaComPessoaSerializer
from utils.utils import formatar_data, converter_string_para_data
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
                
                atividades = Atividade.objects.filter(fase_atividade=f,atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id).distinct()
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

@api_view(['POST'])
def alocar_horas(request, format=None):
    
    atividade_profissional = None
    if 'atividade_profissional' in request.data:
        atividade_profissional = AtividadeProfissional.objects.get(pk=request.data['atividade_profissional']['id'])
        del request.data['atividade_profissional']
    
    tipo_alocacao = None
    if 'tipo_alocacao' in request.data:
        tipo_alocacao = TipoAlocacao.objects.get(pk=request.data['tipo_alocacao']['id'])
        del request.data['tipo_alocacao']
    
    alocacao_horas = AlocacaoHoras(**request.data)
    alocacao_horas.atividade_profissional = atividade_profissional
    alocacao_horas.data_informada = converter_string_para_data(request.data['data_informada'])
    alocacao_horas.data_alocacao = datetime.datetime.now()
    alocacao_horas.tipo_alocacao = tipo_alocacao
    alocacao_horas.save();
    
    horas_alocadas_milisegundos = request.data['horas_alocadas_milisegundos']
    percentual_concluido = request.data['percentual_concluido']    
    
    if (atividade_profissional.horas_alocadas_milisegundos):
        atividade_profissional.horas_alocadas_milisegundos += horas_alocadas_milisegundos
    else:
        atividade_profissional.horas_alocadas_milisegundos = horas_alocadas_milisegundos
    
    quantidade_horas_milisegundos = atividade_profissional.quantidade_horas * 60 * 60 * 1000
    percentual_calculado = (atividade_profissional.horas_alocadas_milisegundos * 100) / quantidade_horas_milisegundos 
    
    if percentual_calculado > 100:
        percentual_calculado = 100
    
    atividade_profissional.percentual_calculado = percentual_calculado
    atividade_profissional.percentual_concluido = percentual_concluido
    atividade_profissional.save();
    
    #Calcular percentual atividade
    atividade = Atividade.objects.filter(atividadeprofissional = atividade_profissional)[0]
    atividades_profissionais = AtividadeProfissional.objects.filter(atividade = atividade)
    percentual_calculado = sum((a.percentual_calculado if a.percentual_calculado else 0) for a in atividades_profissionais) / len(atividades_profissionais);
    percentual_concluido = sum((a.percentual_concluido if a.percentual_concluido else 0) for a in atividades_profissionais) / len(atividades_profissionais);

    atividade.percentual_calculado = percentual_calculado
    atividade.percentual_concluido = percentual_concluido
    atividade.save();
    
    #calcular percentual fase_atividade
    fase_atividade = FaseAtividade.objects.filter(atividade = atividade)[0]
    atividades = Atividade.objects.filter(fase_atividade = fase_atividade)
    percentual_calculado = sum((a.percentual_calculado if a.percentual_calculado else 0) for a in atividades) / len(atividades);
    percentual_concluido = sum((a.percentual_concluido if a.percentual_concluido else 0) for a in atividades) / len(atividades);
    
    fase_atividade.percentual_calculado = percentual_calculado
    fase_atividade.percentual_concluido = percentual_concluido
    fase_atividade.save()
    
    demanda = Demanda.objects.filter(faseatividade = fase_atividade)[0]
    fase_atividades = FaseAtividade.objects.filter(demanda = demanda)
    percentual_calculado = sum((a.percentual_calculado if a.percentual_calculado else 0) for a in fase_atividades) / len(fase_atividades);
    percentual_concluido = sum((a.percentual_concluido if a.percentual_concluido else 0) for a in fase_atividades) / len(fase_atividades);
    
    demanda.percentual_calculado = percentual_calculado
    demanda.percentual_concluido = percentual_concluido
    demanda.save()
    
    return Response(AtividadeProfissionalSerializer(atividade_profissional).data)

@api_view(['GET'])
def buscar_ultima_alocacao(request, atividade_profissional_id, format=None):
    
    alocacao_horas = AlocacaoHoras.objects.filter(atividade_profissional__id = atividade_profissional_id).order_by('-id')[:1]
    if alocacao_horas:
        return Response(AlocacaoHorasSerializer(alocacao_horas[0]).data)
    else:
        return Response({})
    
@api_view(['GET'])
def buscar_atividade_profissional_por_atividade(request, atividade_id, format=None):
    
    atividade_profissional =  AtividadeProfissional.objects.filter(atividade__id = atividade_id, pessoa_fisica__prestador__usuario__id=request.user.id)[:1]
    atividade_profissional_dict = AtividadeProfissionalSerializer(atividade_profissional[0]).data
    
    return Response(atividade_profissional_dict)
