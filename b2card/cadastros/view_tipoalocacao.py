from django.shortcuts import render
from cadastros.models import TipoAlocacao
from cadastros import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

def index(request):
    return render(request, 'tipoalocacao/index.html');

class TipoAlocacaoList(APIView):
    def get(self, request, format=None):
        tipo_alocacao = TipoAlocacao.objects.all().order_by('descricao')
        serializer = serializers.TipoAlocacaoSerializer(tipo_alocacao, many=True)
        return Response(serializer.data)
    
class TipoAlocacaoDetail(APIView):
    def post(self, request, format=None):
        tipo_alocacao = TipoAlocacao(**request.data)
        tipo_alocacao.save()
        serializer = serializers.TipoAlocacaoSerializer(tipo_alocacao)
        return Response(serializer.data)
    
    def delete(self, request, tipohora_id, format=None):
        tipo_alocacao = TipoAlocacao.objects.get(pk=tipohora_id)
        tipo_alocacao.delete()
        serializer = serializers.TipoAlocacaoSerializer(tipo_alocacao)
        return Response(serializer.data)    