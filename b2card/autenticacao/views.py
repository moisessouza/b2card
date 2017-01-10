from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from cadastros.models import Pessoa
from autenticacao.models import GrupoURL
from datetime import datetime
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
def index(request):
    return render(request, 'autenticacao/index.html')

def executar(request):
    username = request.POST['login']
    password = request.POST['senha']
    
    user = authenticate(username=username, password=password)
    if user is not None:
        
        if user.is_superuser:
            login(request, user)
            return redirect('inicial:inicial')
        
        data_atual = datetime.now().date()
        pessoa = Pessoa.objects.filter(Q(pessoafisica__prestador__data_fim__isnull=True) | Q(pessoafisica__prestador__data_fim__gte=data_atual), 
            status='A', pessoafisica__prestador__usuario=user, pessoafisica__prestador__data_inicio__lte=data_atual)
            
        if pessoa:
            login(request, user)
            return redirect('inicial:inicial')
        else:
            return redirect('autenticacao:index')

    else:
        return redirect('autenticacao:index')
        
def logout_view(request):
    logout(request)
    return redirect('autenticacao:index')

def not_permitted(request):
    return render(request, 'autenticacao/not_permitted.html')


@api_view(['GET'])
def verificar_permissoes_abas(request):
    
    grupo_urls = GrupoURL.objects.filter(grupo__user__id=request.user.id, url__contains='#')
    
    abas = []
    
    for i in grupo_urls:
        url = i.url
        aba = url[url.index('#'):len(url)]
        abas.append(aba)
        
    return Response(abas)