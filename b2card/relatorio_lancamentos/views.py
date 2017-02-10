from django.shortcuts import render
from rest_framework.decorators import api_view
from demandas.models import AlocacaoHoras
from utils.utils import converter_string_para_data
from demandas.serializers import AlocacaoHorasSerializer
from rest_framework.response import Response

# Create your views here.

def index(request):
    return render(request, 'relatorio_lancamentos/index.html')


@api_view(['POST'])
def pesquisar_alocacoes_horas(request, format=None):
    
    periodo = request.data['periodo']
    periodo = converter_string_para_data(periodo)
    
    alocacao_horas = AlocacaoHoras.objects.filter(data_informada__month=periodo.month, data_informada__year=periodo.year)
    
    return Response(AlocacaoHorasSerializer(alocacao_horas, many=True).data)
        
        
    
    
    