'''
    Middleware para verificacao de autenticacao
'''
import os
from django.shortcuts import redirect
import importlib

class AuthenticationB2CardMiddleware(object):

    urls_permited = importlib.import_module(os.environ['DJANGO_SETTINGS_MODULE']).URL_PER
    base_url = importlib.import_module(os.environ['DJANGO_SETTINGS_MODULE']).BASE_URL
    
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.path in self.urls_permited:
            return self.get_response(request)


        if request.user.is_authenticated:
            if request.path == self.base_url:
                response = redirect('inicial:inicial')
            else:
                response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        else:
            response = redirect('autenticacao:index')
            
        return response