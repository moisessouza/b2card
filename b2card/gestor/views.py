from django.shortcuts import render
from rest_framework.decorators import api_view
from demandas.models import Demanda
from django.db.models import Q
from cadastros.models import PessoaJuridica
from cadastros.serializers_pessoa import PessoaJuridicaSerializer
from utils.utils import serializarDemandaObject
from rest_framework.response import Response

# Create your views here.
def index(request):
    return render(request, 'gestor/index.html')

@api_view(['GET'])
def buscar_clientes_demandas(request, format=None):
    
    clientes = PessoaJuridica.objects.filter(Q(demanda__responsavel__prestador__usuario__id=request.user.id) | Q(demanda__analista_tecnico_responsavel__prestador__usuario__id=request.user.id)).distinct()
    
    cliente_list = []
    
    for i in clientes:
        cliente = PessoaJuridicaSerializer(i).data

        demandas = Demanda.objects.filter(Q(cliente = i), Q(responsavel__prestador__usuario__id=request.user.id) | Q(analista_tecnico_responsavel__prestador__usuario__id=request.user.id))
        demanda_list = []
        
        for d in demandas:
            demanda = serializarDemandaObject(d)
            demanda_list.append(demanda)
            
        cliente['demandas'] = demanda_list
        cliente_list.append(cliente)
        
    return Response(cliente_list)