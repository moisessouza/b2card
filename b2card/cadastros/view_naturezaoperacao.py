from django.shortcuts import render
from cadastros.models import TipoHora, NaturezaOperacao
from cadastros import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

def index(request):
    return render(request, 'natureza_operacao/index.html');

class NaturezaOperacaoList(APIView):
    def get(self, request, format=None):
        natureza_operacao = NaturezaOperacao.objects.all().order_by('nome')
        serializer = serializers.NaturezaOperacaoSerializer(natureza_operacao, many=True)
        return Response(serializer.data)
    
class NaturezaOperacaoDetail(APIView):
    def post(self, request, format=None):
        
        natureza_operacao = NaturezaOperacao(**request.data)
        natureza_operacao.save()
                
        serializer = serializers.NaturezaOperacaoSerializer(natureza_operacao)
        return Response(serializer.data)
    
    def delete(self, request, naturezaoperacao_id, format=None):
        natureza_operacao = NaturezaOperacao.objects.get(pk=naturezaoperacao_id)
        natureza_operacao.delete()
        serializer = serializers.NaturezaOperacaoSerializer(natureza_operacao)
        return Response(serializer.data)    
