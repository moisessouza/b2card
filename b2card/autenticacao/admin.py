from django.contrib import admin
from autenticacao.models import GrupoURL
# Register your models here.

class GrupoUrlAdmin(admin.ModelAdmin):
    list_display = ('url', 'grupo')
    ordering = ('url',)
    list_filter = ('url', 'grupo__name')
    
admin.site.register(GrupoURL, GrupoUrlAdmin)
