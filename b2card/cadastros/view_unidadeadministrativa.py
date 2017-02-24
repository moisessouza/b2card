from django.shortcuts import render
from cadastros.models import UnidadeAdministrativa, PessoaFisica
from cadastros import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.utils import converter_string_para_float
from rest_framework.decorators import api_view
from cadastros.serializers import UnidadeAdministrativaSerializer

def index(request):
    return render(request, 'unidade_administrativa/index.html');

class UnidadeAdministrativaList(APIView):
    def get(self, request, format=None):
        unidade_administrativa = UnidadeAdministrativa.objects.all().order_by('codigo', 'nome')
        serializer = serializers.UnidadeAdministrativaSerializer(unidade_administrativa, many=True)
        return Response(serializer.data)
    
class UnidadeAdministrativaDetail(APIView):
    def post(self, request, format=None):
        
        unidade_administrativa = UnidadeAdministrativa(**request.data)
        unidade_administrativa.custo_operacao_hora = converter_string_para_float(unidade_administrativa.custo_operacao_hora)
        unidade_administrativa.save()
                
        serializer = serializers.UnidadeAdministrativaSerializer(unidade_administrativa)
        return Response(serializer.data)
    
    def delete(self, request, unidade_administrativa_id, format=None):
        unidade_administrativa = UnidadeAdministrativa.objects.get(pk=unidade_administrativa_id)
        unidade_administrativa.delete()
        serializer = serializers.UnidadeAdministrativaSerializer(unidade_administrativa)
        return Response(serializer.data)
    
@api_view(['GET'])
def buscar_unidade_administrativa_por_pessoa(request, format=None):
    
    if request.user.is_superuser:
        return UnidadeAdministrativaList.get(request, format)
    else:
        pessoa_fisica = PessoaFisica.objects.filter(prestador__usuario__id = request.user.id)[0]
        unidade_administrativas = pessoa_fisica.unidade_administrativas.all().order_by('codigo', 'nome')
        return Response(UnidadeAdministrativaSerializer(unidade_administrativas, many=True).data)