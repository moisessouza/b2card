from django.shortcuts import render
from cadastros.models import TipoHora, CentroCusto, ValorHora
from cadastros import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from cadastros.serializers import ValorHoraSerializer

def index(request):
    return render(request, 'centro_custo/index.html');

class CentroCustoList(APIView):
    def get(self, request, format=None):
        centro_custos = CentroCusto.objects.all().order_by('nome')
        serializer = serializers.CentroCustoSerializer(centro_custos, many=True)
        return Response(serializer.data)
    
class CentroCustoDetail(APIView):
    def post(self, request, format=None):
        
        centro_custo = CentroCusto(**request.data)
        centro_custo.save()
                
        serializer = serializers.CentroCustoSerializer(centro_custo)
        return Response(serializer.data)
    
    def delete(self, request, centrocusto_id, format=None):
        centro_custo = CentroCusto.objects.get(pk=centrocusto_id)
        centro_custo.delete()
        serializer = serializers.CentroCustoSerializer(centro_custo)
        return Response(serializer.data)   