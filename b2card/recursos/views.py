from django.shortcuts import render, redirect
from recursos.models import Funcionario, Cargo
from recursos.forms import FuncionarioForm
from rest_framework.views import APIView
from recursos import serializers
from rest_framework.response import Response
from recursos.serializers import CargoSerializer, FuncionarioSerializer
from datetime import datetime
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from cadastros.serializers_pessoa import UserSerializer
from cadastros.models import Prestador



# Create your views here.
def index(request):
    
    funcionarios = Funcionario.objects.all()
    
    context = {
        'funcionarios': funcionarios
    }

    return render(request, 'recursos/index.html', context)

def novo(request):
    return render(request, 'recursos/funcionario.html')

def editar(request, cliente_id):
    
    funcionario = Funcionario.objects.get(pk=cliente_id)
    
    context = {
        'funcionario': funcionario
    }

    return render(request, 'recursos/funcionario.html', context)

def executar(request):
    
    if 'gravar' in request.POST:
    
        if 'id' in request.POST and request.POST['id']:
            funcionario = Funcionario.objects.get(pk=request.POST['id'])
            form = FuncionarioForm(request.POST, instance=funcionario)
        else:
            form = FuncionarioForm(request.POST)
        form.save()
        
        context = {
            'success':{
                'message': 'Funcionario gravado com sucesso!'
            }
        }
        
        return render(request, 'recursos/funcionario.html', context)
    
    elif 'deletar' in request.POST:
        funcionario = Funcionario.objects.get(pk=request.POST['id'])
        funcionario.delete()
        return redirect('recursos:inicial')
    
''' 
    API REST
''' 
class FuncionarioList(APIView):
    def get(self, request, format=None):
        funcionarios = Funcionario.objects.all()
        serializer = serializers.FuncionarioSerializer(funcionarios, many=True)
        return Response(serializer.data)
    
class FuncionarioDetail(APIView):
    def get(self, request, funcionario_id, format=None):
        funcionario = Funcionario.objects.get(pk=funcionario_id)
        serializer = serializers.FuncionarioSerializer(funcionario)
        
        data = serializer.data
        
        iso = funcionario.data_admissao.isoformat()
        tokens = iso.strip()
        tokens = iso.split('-')
        
        data['data_admissao'] = "%s/%s/%s" % (tokens[2],tokens[1],tokens[0])
        
        return Response(data)
    def post(self, request, format=None):
        
        if 'id' in request.data:
            funcionario = Funcionario.objects.get(pk=request.data['id']);
        else:
            funcionario = Funcionario();
        
        funcionario.nome = request.data['nome']
        
        cargo = request.data['cargo']
        cargo = Cargo.objects.get(pk=cargo['id'])
        
        funcionario.cargo = cargo
        funcionario.cpf = request.data['cpf']
        funcionario.rg = request.data['rg']
        funcionario.endereco = request.data['endereco']
        funcionario.cidade = request.data['cidade']
        funcionario.estado = request.data['estado']
        funcionario.cep = request.data['cep']
        
        salario = request.data['salario']
        funcionario.salario = salario
        
        data_string = request.data['data_admissao']
        
        data_admissao = datetime.strptime(data_string, '%d/%m/%Y')
        funcionario.data_admissao = data_admissao.date()
        
        funcionario.save()
        
        serializer = FuncionarioSerializer(funcionario)
            
        return Response(serializer.data)
    
    def delete(self, request, funcionario_id):
        funcionario = Funcionario.objects.get(pk=funcionario_id)
        funcionario.delete()
        
        serializer = FuncionarioSerializer(funcionario)
        
        return Response(serializer.data)
        
    
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