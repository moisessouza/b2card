from django.contrib import admin
from autenticacao.models import GrupoURL
# Register your models here.

class GrupoUrlAdmin(admin.ModelAdmin):
    list_display = ('grupo', 'url')
    
admin.site.register(GrupoURL, GrupoUrlAdmin)
