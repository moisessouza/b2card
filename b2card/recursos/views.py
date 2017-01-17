from django.shortcuts import render, redirect
from recursos.models import Cargo
from rest_framework.views import APIView
from recursos import serializers
from rest_framework.response import Response
from recursos.serializers import CargoSerializer
from datetime import datetime
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from cadastros.serializers_pessoa import UserSerializer
from cadastros.models import Prestador
    
class CargoList(APIView):
    def get(self, request, format=None):
        cargos = Cargo.objects.all()
        serializer = serializers.CargoSerializer(cargos, many=True)
        return Response(serializer.data)
    
class CargoDetail(APIView):
    def get(self, request, cargo_id, format=None):
        cargo = Cargo.objects.get(pk=cargo_id)
        serializer = serializers.CargoSerializer(cargo)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        
        if 'id' in request.data:
            cargo = Cargo.objects.get(pk=request.data['id'])
            serializer = serializers.CargoSerializer(cargo, data=request.data);
        else:
            serializer = serializers.CargoSerializer(data=request.data);    
        
        if serializer.is_valid(raise_exception=True):
            serializer.save();
            
        return Response(serializer.data)
    
    def delete(self, request, cargo_id, format=None):
        cargo = Cargo.objects.get(pk=cargo_id)
        cargo.delete();
        
        serializer = serializers.CargoSerializer(cargo)
        return Response(serializer.data)
    
@api_view(['GET'])
def buscar_usuarios_nao_usados(request, format=None):
    usuarios = User.objects.all()
    usuarios_list = []
    
    for i in usuarios:
        prestador = Prestador.objects.filter(usuario = i)
        if len(prestador) == 0:
            usuarios_list.append(i)
    data = UserSerializer(usuarios_list, many=True).data
       
    return Response(data)

@api_view(['GET'])
def buscar_usuario_prestador(request, prestador_id, format=None):
    usuario = User.objects.filter(prestador__id=prestador_id)
    return Response(UserSerializer(usuario, many=True).data)