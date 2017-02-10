from django.shortcuts import render
from rest_framework.decorators import api_view
from demandas.models import AlocacaoHoras
from utils.utils import converter_string_para_data
from demandas.serializers import AlocacaoHorasSerializer,\
    RelatorioAlocacaoHorasSerializer
from rest_framework.response import Response

# Create your views here.

def index(request):
    return render(request, 'relatorio_lancamentos/index.html')


@api_view(['POST'])
def pesquisar_alocacoes_horas(request, format=None):
    
    periodo = request.data['periodo']
    periodo = converter_string_para_data(periodo)
    
    alocacao_horas = AlocacaoHoras.objects.filter(data_informada__month=periodo.month, data_informada__year=periodo.year)
    
    if 'profissional_id' in request.data and request.data['profissional_id']:
        alocacao_horas = alocacao_horas.filter(atividade_profissional__pessoa_fisica__id=request.data['profissional_id'])
        
    if 'cliente_id' in request.data and request.data['cliente_id']:
        alocacao_horas = alocacao_horas.filter(atividade_profissional__atividade__fase_atividade__demanda__cliente__id=request.data['cliente_id'])
        
    if 'status_demanda' in request.data and request.data['status_demanda']:
        alocacao_horas = alocacao_horas.filter(atividade_profissional__atividade__fase_atividade__demanda__status_demanda=request.data['status_demanda'])
        
    if 'demanda' in request.data and request.data['demanda']:
        alocacao_horas = alocacao_horas.filter(atividade_profissional__atividade__fase_atividade__demanda__id=request.data['demanda']['id'])
        
    return Response(RelatorioAlocacaoHorasSerializer(alocacao_horas, many=True).data)
        
        
    
    
    