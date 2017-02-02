from django.shortcuts import render
from cadastros.models import TipoHora, Fase
from cadastros import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

def index(request):
    return render(request, 'fase/index.html');

class FaseList(APIView):
    def get(self, request, format=None):
        fases = Fase.objects.all().order_by('descricao')
        serializer = serializers.FaseSerializer(fases, many=True)
        return Response(serializer.data)
    
class FaseDetail(APIView):
    def post(self, request, format=None):
        
        fase = Fase(**request.data)
        fase.save()
                
        serializer = serializers.FaseSerializer(fase)
        return Response(serializer.data)
    
    def delete(self, request, tipohora_id, format=None):
        fase = Fase.objects.get(pk=tipohora_id)
        fase.delete()
        serializer = serializers.FaseSerializer(fase)
        return Response(serializer.data)    