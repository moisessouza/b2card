'''
    Middleware para verificacao de autenticacao
'''

from django.shortcuts import redirect

class AuthenticationB2CardMiddleware(object):
    
    urls_permited = ['/autenticacao/', '/autenticacao/login/']
    
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if request.path in self.urls_permited:
            return self.get_response(request)


        if request.user.is_authenticated:
            if request.path == '/':
                response = redirect('inicial:inicial')
            else:
                response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.

        else:
            response = redirect('autenticacao:index')
            
        return response