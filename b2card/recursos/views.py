from django.shortcuts import render, redirect
from recursos.models import Funcionario, Cargo
from recursos.forms import FuncionarioForm
from rest_framework.views import APIView
from recursos import serializers
from rest_framework.response import Response
from recursos.serializers import CargoSerializer, FuncionarioSerializer



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
        return Response(serializer.data)
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
        funcionario.salario = request.data['salario']
        
        funcionario.save()
        
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