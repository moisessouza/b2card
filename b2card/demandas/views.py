from django.shortcuts import render

# Create your views here.

def index(request):
    context = {}
    return render(request, 'demandas/index.html', context)
    
def novo(request):
    return render(request, 'demandas/demanda.html')