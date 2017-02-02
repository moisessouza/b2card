from django.shortcuts import render
from cadastros.models import NaturezaDemanda
from cadastros import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

def index(request):
    return render(request, 'naturezademanda/index.html');

class NaturezaDemandaList(APIView):
    def get(self, request, format=None):
        natureza_demandas = NaturezaDemanda.objects.all().order_by('descricao')
        serializer = serializers.NaturezaDemandaSerializer(natureza_demandas, many=True)
        return Response(serializer.data)
    
class NaturezaDemandaDetail(APIView):
    def post(self, request, format=None):
        
        natureza_demanda = NaturezaDemanda(**request.data)
        natureza_demanda.save()
                
        serializer = serializers.NaturezaDemandaSerializer(natureza_demanda)
        return Response(serializer.data)
    
    def delete(self, request, naturezademanda_id, format=None):
        natureza_demanda = NaturezaDemanda.objects.get(pk=naturezademanda_id)
        natureza_demanda.delete()
        serializer = serializers.NaturezaDemandaSerializer(natureza_demanda)
        return Response(serializer.data)    