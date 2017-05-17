from django.shortcuts import render
from cadastros.models import TipoHora, Fase, CentroResultado
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
        
        centro_resultado = None
        if 'centro_resultado' in request.data:
            if request.data['centro_resultado'] and 'id' in request.data['centro_resultado']:
                centro_resultado = CentroResultado.objects.get(pk=request.data['centro_resultado']['id'])
            del request.data['centro_resultado']
        
        fase = Fase(**request.data)
        fase.centro_resultado = centro_resultado
        fase.save()
                
        serializer = serializers.FaseSerializer(fase)
        return Response(serializer.data)
    
    def delete(self, request, fase_id, format=None):
        fase = Fase.objects.get(pk=fase_id)
        fase.delete()
        serializer = serializers.FaseSerializer(fase)
        return Response(serializer.data)    