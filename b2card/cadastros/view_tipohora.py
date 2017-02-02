from django.shortcuts import render
from cadastros.models import TipoHora
from cadastros import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

def index(request):
    return render(request, 'tipo_hora/index.html');

class TipoHoraList(APIView):
    def get(self, request, format=None):
        tipohoras = TipoHora.objects.all().order_by('descricao')
        serializer = serializers.TipoHoraSerializer(tipohoras, many=True)
        return Response(serializer.data)
    
class TipoHoraDetail(APIView):
    def post(self, request, format=None):
        
        tipo_hora = TipoHora(**request.data)
        tipo_hora.save()
                
        serializer = serializers.TipoHoraSerializer(tipo_hora)
        return Response(serializer.data)
    
    def delete(self, request, tipohora_id, format=None):
        tipo_hora = TipoHora.objects.get(pk=tipohora_id)
        tipo_hora.delete()
        serializer = serializers.TipoHoraSerializer(tipo_hora)
        return Response(serializer.data)    