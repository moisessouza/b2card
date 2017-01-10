'''
Created on 6 de jan de 2017

@author: moises
'''
from django import template
import re
from autenticacao.models import GrupoURL
from django.shortcuts import resolve_url
from django.core.cache import cache
from autenticacao.middleware import CACHE_GRUPOS

register = template.Library()

@register.tag('check_permittion')
def check_permittion(parser, token):
    r = re.compile('.*\s\'([a-z]+\:[a-z]+)\'')
    url_name = r.match(token.contents).group(1)
    nodelist = parser.parse(('endcheck_permittion',))
    parser.delete_first_token()
    return CheckNode(nodelist, url_name)

class CheckNode(template.Node):
    url_name = None
    
    def __init__(self, nodelist, url_name):
        self.url_name = url_name
        self.nodelist = nodelist
        pass
    def render(self, context):
        user = context.request.user
        
        has_permission = False
        
        if user.is_superuser:
            has_permission = True
        else:
            grupo_urls = None
            if user.id in CACHE_GRUPOS:
                grupo_urls = CACHE_GRUPOS[user.id]
            else:
                grupo_urls = GrupoURL.objects.filter(grupo__user__id=user.id, 
                    grupo__user__prestador__pessoa_fisica__pessoa__status='A')
                CACHE_GRUPOS[user.id] = grupo_urls
            
            url = resolve_url(self.url_name)
            for i in grupo_urls:
                if i.url in url:
                    has_permission = True
                    break
        
        if has_permission:
            output = self.nodelist.render(context)
            return output
        else:
            return '';
