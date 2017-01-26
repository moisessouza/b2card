from django.shortcuts import render
from rest_framework.decorators import api_view
from demandas.models import Demanda, FaseAtividade
from django.db.models import Q
from cadastros.models import PessoaJuridica
from cadastros.serializers_pessoa import PessoaJuridicaSerializer
from utils.utils import serializarDemandaObject, serializar_fase_atividade
from rest_framework.response import Response
from demandas.serializers import DemandaSerializer

# Create your views here.
def index(request):
    return render(request, 'gestor/index.html')

@api_view(['GET'])
def buscar_clientes_demandas(request, format=None):
    
    clientes = PessoaJuridica.objects.filter(Q(demanda__responsavel__prestador__usuario__id=request.user.id) | Q(demanda__analista_tecnico_responsavel__prestador__usuario__id=request.user.id)).distinct()
    
    cliente_list = []
    demanda_select = []
    
    for i in clientes:
        cliente = PessoaJuridicaSerializer(i).data

        demandas = Demanda.objects.filter(Q(cliente = i), Q(responsavel__prestador__usuario__id=request.user.id) | Q(analista_tecnico_responsavel__prestador__usuario__id=request.user.id))
        demanda_list = []
        
        for d in demandas:
            demanda = serializarDemandaObject(d)
            demanda_list.append(demanda)
            demanda_select.append(d)
            
        cliente['demandas'] = demanda_list
        cliente_list.append(cliente)
        
    # buscar responsavel fase
    clientes = PessoaJuridica.objects.filter(demanda__faseatividade__responsavel__prestador__usuario__id=request.user.id).distinct()
    for i in clientes:
        cliente = PessoaJuridicaSerializer(i).data
        demandas = Demanda.objects.filter(cliente = i, faseatividade__responsavel__prestador__usuario__id=request.user.id).exclude(id__in=[d.id for d in demanda_select])
        
        demanda_list = []
        for d in demandas:
            demanda_dict = DemandaSerializer(d).data
            
            fase_atividades = FaseAtividade.objects.filter(demanda = d, responsavel__prestador__usuario__id=request.user.id)
            fase_atividade_list = serializar_fase_atividade(fase_atividades)
            
            demanda_dict['fase_atividades'] = fase_atividade_list
            demanda_list.append(demanda_dict)
            
        cliente['demandas'] = demanda_list
        cliente_list.append(cliente)
        
        
    return Response(cliente_list)