from django.shortcuts import render
from cadastros.models import TipoHora, ContaGerencial
from cadastros import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

def index(request):
    return render(request, 'conta_gerencial/index.html');

class ContaGerencialList(APIView):
    def get(self, request, format=None):
        conta_gerencial = ContaGerencial.objects.all()
        serializer = serializers.ContaGerencialSerializer(conta_gerencial, many=True)
        return Response(serializer.data)
    
class ContaGerencialDetail(APIView):
    def post(self, request, format=None):
        
        conta_gerencial = ContaGerencial(**request.data)
        conta_gerencial.save()
                
        serializer = serializers.ContaGerencialSerializer(conta_gerencial)
        return Response(serializer.data)
    
    def delete(self, request, contagerencial_id, format=None):
        conta_gerencial = ContaGerencial.objects.get(pk=contagerencial_id)
        conta_gerencial.delete()
        serializer = serializers.ContaGerencialSerializer(conta_gerencial)
        return Response(serializer.data)    
