from django.shortcuts import render
from cadastros.models import UnidadeAdministrativa
from cadastros import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

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
        unidade_administrativa.save()
                
        serializer = serializers.UnidadeAdministrativaSerializer(unidade_administrativa)
        return Response(serializer.data)
    
    def delete(self, request, unidade_administrativa_id, format=None):
        unidade_administrativa = UnidadeAdministrativa.objects.get(pk=unidade_administrativa_id)
        unidade_administrativa.delete()
        serializer = serializers.UnidadeAdministrativaSerializer(unidade_administrativa)
        return Response(serializer.data)    
