from django.shortcuts import render, redirect
from recursos.models import Funcionario
from recursos.forms import FuncionarioForm
from rest_framework.views import APIView
from recursos import serializers
from rest_framework.response import Response

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