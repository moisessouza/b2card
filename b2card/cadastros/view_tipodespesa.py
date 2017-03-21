from django.shortcuts import render
from cadastros.models import TipoDespesa
from cadastros import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

def index(request):
    return render(request, 'tipodespesa/index.html');

class TipoDespesaList(APIView):
    def get(self, request, format=None):
        tipo_despesa = TipoDespesa.objects.all().order_by('descricao')
        serializer = serializers.TipoDespesaSerializer(tipo_despesa, many=True)
        return Response(serializer.data)
    
class TipoDespesaDetail(APIView):
    def post(self, request, format=None):
        tipo_despesa = TipoDespesa(**request.data)
        tipo_despesa.save()
        serializer = serializers.TipoDespesaSerializer(tipo_despesa)
        return Response(serializer.data)
    
    def delete(self, request, tipodespesa_id, format=None):
        tipo_despesa = TipoDespesa.objects.get(pk=tipodespesa_id)
        tipo_despesa.delete()
        serializer = serializers.TipoDespesaSerializer(tipo_despesa)
        return Response(serializer.data)    