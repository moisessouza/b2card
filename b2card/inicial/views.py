from django.shortcuts import render
from rest_framework.decorators import api_view
from demandas.models import Atividade, Demanda, FaseAtividade,\
    AtividadeProfissional
from demandas.serializers import DemandaSerializer, AtividadeSerializer,\
    FaseAtividadeSerializer, AtividadeProfissionalSerializer
from rest_framework.response import Response
from cadastros.models import PessoaJuridica
from cadastros.serializers_pessoa import PessoaJuridicaSerializer

# Create your views here.
def index (request):
    return render(request, 'first_page.html')

@api_view(['GET'])
def buscar_atividades_usuario(request, format=None):

    clientes  = PessoaJuridica.objects.filter(demanda__faseatividade__atividade__atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id)

    cliente_list = [];

    for c in clientes:

        cliente_dict = PessoaJuridicaSerializer(c).data

        demandas = Demanda.objects.filter(cliente = c, faseatividade__atividade__atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id);
        demanda_list = []
        
        for i in demandas:
    
            demanda_dict = DemandaSerializer(i).data
            demanda_list.append(demanda_dict)
            
            fase_atividade_list = []
            fase_atividades = FaseAtividade.objects.filter(demanda__in=demandas, atividade__atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id);
            
            for f in fase_atividades:
                
                fase_atividade_dict = FaseAtividadeSerializer(f).data
                fase_atividade_list.append(fase_atividade_dict)
                
                atividades = Atividade.objects.filter(fase_atividade=f,atividadeprofissional__pessoa_fisica__prestador__usuario__id=request.user.id)
                atividade_list = [];
                
                for a in atividades:
                    
                    atividade_dict = AtividadeSerializer(a).data
                    atividade_list.append(atividade_dict)
                    atividade_profissional =  AtividadeProfissional.objects.filter(atividade = a, pessoa_fisica__prestador__usuario__id=request.user.id)[:1]
                    
                    atividade_profissional_dict = AtividadeProfissionalSerializer(atividade_profissional[0]).data
                    atividade_dict['atividade_profissional'] = atividade_profissional_dict
                    
                fase_atividade_dict['atividades']=atividade_list
                    
            demanda_dict['fase_atividades']=fase_atividade_list       
        
        cliente_dict['demandas'] = demanda_list
        
        cliente_list.append(cliente_dict)
        
    return Response(cliente_list)
