from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

# Create your views here.
def index(request):
    return render(request, 'autenticacao/index.html')

def executar(request):
    username = request.POST['login']
    password = request.POST['senha']
    
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('inicial:inicial')
        # Redirect to a success page.
    else:
        return redirect('autenticacao:index')
        
def logout_view(request):
    logout(request)
    return redirect('autenticacao:index')