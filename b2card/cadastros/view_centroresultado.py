from django.shortcuts import render
from cadastros.models import TipoHora, CentroResultado
from cadastros import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

def index(request):
    return render(request, 'centro_resultado/index.html');

class CentroResultadoList(APIView):
    def get(self, request, format=None):
        centro_resultados = CentroResultado.objects.all()
        serializer = serializers.CentroResultadoSerializer(centro_resultados, many=True)
        return Response(serializer.data)
    
class CentroResultadoDetail(APIView):
    def post(self, request, format=None):
        
        centro_resultado = CentroResultado(**request.data)
        centro_resultado.save()
                
        serializer = serializers.CentroResultadoSerializer(centro_resultado)
        return Response(serializer.data)
    
    def delete(self, request, centroresultado_id, format=None):
        centro_resultado = CentroResultado.objects.get(pk=centroresultado_id)
        centro_resultado.delete()
        serializer = serializers.CentroResultadoSerializer(centro_resultado)
        return Response(serializer.data)    
