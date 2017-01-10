'''
    Middleware para verificacao de autenticacao
'''
import os
from django.shortcuts import redirect
import importlib
from autenticacao.models import GrupoURL

CACHE_GRUPOS = {}

class AuthenticationB2CardMiddleware(object):

    urls_permited = importlib.import_module(os.environ['DJANGO_SETTINGS_MODULE']).URL_PER
    base_url = importlib.import_module(os.environ['DJANGO_SETTINGS_MODULE']).BASE_URL
    
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        grupo_urls = GrupoURL.objects.filter(grupo__user__id=request.user.id, 
                                grupo__user__prestador__pessoa_fisica__pessoa__status='A')
                    
        CACHE_GRUPOS[request.user.id] = grupo_urls

        if request.path in self.urls_permited:
            return self.get_response(request)

        if '/api/' in request.path: 
            return self.get_response(request)
        
        if request.user.is_authenticated:
            if request.path == self.base_url:
                response = redirect('inicial:inicial')
            else:
                if request.user.is_superuser:
                    response = self.get_response(request)
                else:
                    
                    has_permission = False
                    
                    for i in grupo_urls:
                        if i.url in request.path:
                            has_permission = True
                            break
                        
                    if has_permission:
                        response = self.get_response(request)
                    else:
                        response = redirect('autenticacao:not_permitted')
                    
        # Code to be executed for each request/response after
        # the view is called.

        else:
            response = redirect('autenticacao:index')
            
        return response