from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from cadastros.models import Pessoa
from autenticacao.models import GrupoURL

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
        
        pessoa = Pessoa.objects.filter(status='A', pessoafisica__prestador__usuario=user)
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
