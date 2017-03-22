from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from cadastros import serializers
from cadastros.models import TipoHora, CentroCusto, Pessoa, TelefonePessoa, \
    EnderecoPessoa, DadosBancariosPessoa, PessoaFisica, Prestador, \
    PessoaJuridica, Contato, TelefoneContato, CentroResultado, \
    UnidadeAdministrativa, ContaGerencial, Apropriacao, NaturezaOperacao, \
    CustoPrestador, Arquivo
from cadastros.serializers_pessoa import PessoaSerializer, \
    EnderecoPessoaSerializer, TelefonePessoaSerializer, \
    DadosBancariosPessoaSerializer, PessoaFisicaSerializer, PrestadorSerializer, \
    PessoaJuridicaSerializer, ContatoSerializer, TelefoneContatoSerializer, \
    ApropriacaoSerializer, CustoPrestadorSerializer,\
    PessoaJuridicaComPessoaSerializer, PessoaFisicaComPessoaSerializer,\
    ArquivoSerializer
from recursos.models import Cargo
from utils.utils import converter_string_para_data, formatar_data, \
    converter_string_para_float
from rest_framework.decorators import api_view
from cadastros.serializers import UnidadeAdministrativaSerializer
import importlib
import os
from django.http.response import HttpResponse


def index(request):
    return render(request, 'pessoa/index.html')

def novo(request):
    return render(request, 'pessoa/cadastro.html')

def editar(request, pessoa_id):
    
    context = {
        'pessoa_id': pessoa_id
    }
    
    return render(request, 'pessoa/cadastro.html', context)
class PessoaList(APIView):
    def get(self, request, format=None):
        pessoas = Pessoa.objects.all().order_by('nome_razao_social')
        data = PessoaSerializer(pessoas, many=True).data
        return Response(data)
    
class PessoaJuridicaList(APIView):
    def get(self, request, format=None):
        pessoas = PessoaJuridica.objects.filter(pessoa__tipo='J')
        data = PessoaJuridicaComPessoaSerializer(pessoas, many=True).data
        return Response(data)
    
class PessoaFisicaList(APIView):
    def get(self, request, format=None):
        pessoas = PessoaFisica.objects.filter(pessoa__tipo='F').order_by('pessoa__nome_razao_social')
        data = PessoaFisicaComPessoaSerializer(pessoas, many=True).data
        return Response(data)
    
class PessoaDetail(APIView):
    
    def get(self, request, pessoa_id, format=None):
        pessoa = Pessoa.objects.get(pk=pessoa_id)
        data = self.serializar_pessoa(pessoa)
        return Response(data)
        
    def post(self, request, format=None):
        
        data = request.data
        
        centro_custo = None
        if 'centro_custo' in data:
            centro_custo = CentroCusto.objects.get(pk = data['centro_custo']['id'])
            del data['centro_custo']
            
        if 'data_contratacao' in data:
            data['data_contratacao']  = converter_string_para_data (data['data_contratacao'])
        
        if 'data_rescisao' in data:
            data['data_rescisao'] = converter_string_para_data(data['data_rescisao'])
            
        if 'data_renegociacao_valor' in data and data['data_renegociacao_valor']:
            data['data_renegociacao_valor'] = converter_string_para_data(data['data_renegociacao_valor'])
        else:
            data['data_renegociacao_valor'] = None
        
        telefones = None 
        if 'telefones' in data:
            telefones = data['telefones']
            del data['telefones']
            
        enderecos = None
        if 'enderecos' in data:
            enderecos = data['enderecos']
            del data['enderecos']
            
        dados_bancarios = None
        if 'dados_bancarios' in data:
            dados_bancarios = data['dados_bancarios']
            del data['dados_bancarios']
            
        pessoa_fisica = None
        if 'pessoa_fisica' in data:
            pessoa_fisica = data['pessoa_fisica']
            del data['pessoa_fisica']
            
        pessoa_juridica = None
        if 'pessoa_juridica' in data:
            pessoa_juridica = data['pessoa_juridica']
            del data['pessoa_juridica']
        
        apropriacao = None
        if 'apropriacao' in data:
            apropriacao = data['apropriacao']
            del data['apropriacao']
            
        pessoa = Pessoa(**data)
        pessoa.centro_custo = centro_custo
        pessoa.save()
        
        self.gravar_telefones(telefones, pessoa)
        self.gravar_enderecos(enderecos, pessoa)
        self.gravar_dados_bancarios(dados_bancarios, pessoa)
        self.gravar_apropriacao(apropriacao, pessoa)
        
        if data['tipo'] == 'F':
            self.gravar_pessoa_fisica(pessoa_fisica, pessoa)
        
        if data['tipo'] == 'J':
            self.gravar_pessoa_juridica(pessoa_juridica, pessoa)
             
        data = self.serializar_pessoa(pessoa)
        
        return Response(data);
    
    def serializar_pessoa(self, pessoa):
        
        data = PessoaSerializer(pessoa).data
        
        data['data_renegociacao_valor'] = formatar_data(pessoa.data_renegociacao_valor)
        data['enderecos'] = self.serializar_enderecos(pessoa)
        data['telefones'] = self.serializar_telefones(pessoa)
        data['dados_bancarios'] = self.serializar_dados_bancarios(pessoa)
        data['pessoa_fisica'] = self.serializar_pessoa_fisica(pessoa)
        data['pessoa_juridica'] = self.serializar_pessoa_juridica(pessoa)
        data['apropriacao'] = self.serializar_apropriacao(pessoa)
        
        return data
    
    def serializar_enderecos (self, pessoa):
        enderecos = EnderecoPessoa.objects.filter(pessoa = pessoa)
        if enderecos:
            return EnderecoPessoaSerializer(enderecos, many=True).data
        return []

    def serializar_telefones(self, pessoa):
        telefones = TelefonePessoa.objects.filter(pessoa = pessoa)
        if telefones:
            return TelefonePessoaSerializer(telefones, many=True).data
        
        return []
    
    def serializar_dados_bancarios(self, pessoa):
        dados_bancarios = DadosBancariosPessoa.objects.filter(pessoa = pessoa)
        if dados_bancarios:
            return DadosBancariosPessoaSerializer(dados_bancarios, many=True).data
        
        return []
    
    def serializar_pessoa_fisica(self, pessoa):
        pessoa_fisica = PessoaFisica.objects.filter(pessoa = pessoa)
        if pessoa_fisica:
            data = PessoaFisicaSerializer(pessoa_fisica[0]).data
            data['data_expedicao'] = formatar_data(pessoa_fisica[0].data_expedicao)
            data['data_nascimento'] = formatar_data(pessoa_fisica[0].data_nascimento)
            data['data_emicao_pis'] = formatar_data(pessoa_fisica[0].data_emicao_pis)
            data['prestadores'] = self.serializar_prestador(pessoa_fisica[0])
            data['custos_prestador'] = self.serializar_custos_prestador(pessoa_fisica[0])
            data['unidade_administrativas'] = self.serializar_unidade_administrativas(pessoa_fisica[0])
            return data
        
        return None
    
    def serializar_unidade_administrativas(self, pessoa_fisica):
        unidade_administrativas = pessoa_fisica.unidade_administrativas.all()
        return UnidadeAdministrativaSerializer(unidade_administrativas, many=True).data
    
    def serializar_custos_prestador(self, pessoa_fisica):
        custos_prestador = CustoPrestador.objects.filter(pessoa_fisica = pessoa_fisica)
        if custos_prestador:
            custo_prestador_list = []
            for custo_prestador in custos_prestador:
                data = CustoPrestadorSerializer(custo_prestador).data
                data['data_inicio'] = formatar_data(custo_prestador.data_inicio)
                data['data_fim'] = formatar_data(custo_prestador.data_fim)
                custo_prestador_list.append(data)
            return custo_prestador_list
        return None

    def serializar_pessoa_juridica(self, pessoa):
        pessoa_juridica = PessoaJuridica.objects.filter(pessoa = pessoa)
        if pessoa_juridica:
            data = PessoaJuridicaSerializer(pessoa_juridica[0]).data
            
            contatos = Contato.objects.filter(pessoa_juridica = pessoa_juridica)
            contatos_list = []

            for contato in contatos:
                data_contato = ContatoSerializer(contato).data
                telefones = TelefoneContato.objects.filter(contato = contato)
                data_contato['telefones'] = TelefoneContatoSerializer(telefones, many=True).data
                contatos_list.append(data_contato)
            
            data['contatos'] = contatos_list
            
            return data
        
        return None
    
    def serializar_prestador(self, pessoa_fisica):
        prestadores = Prestador.objects.filter(pessoa_fisica = pessoa_fisica)
        if prestadores:
            prestador_list = []
            for p in prestadores:
                data = PrestadorSerializer(p).data
                data['data_inicio'] = formatar_data(p.data_inicio)
                data['data_fim'] = formatar_data(p.data_fim)
                data['data_contratacao'] = formatar_data(p.data_contratacao)
                data['data_rescisao'] = formatar_data(p.data_rescisao)
                data['data_fim_aditivo'] = formatar_data(p.data_fim_aditivo)
                data['data_exame_admissional'] = formatar_data(p.data_exame_admissional)
                data['data_exame_demissional'] = formatar_data(p.data_exame_demissional)
                data['data_ultimo_exame_periodico'] = formatar_data(p.data_ultimo_exame_periodico)
                data['data_ultima_avaliacao'] = formatar_data(p.data_ultima_avaliacao)
                data['data_proxima_avaliacao'] = formatar_data(p.data_proxima_avaliacao)
                prestador_list.append(data)
            return prestador_list
        
        return None
    
    def serializar_apropriacao(self, pessoa):
        apropriacao = Apropriacao.objects.filter(pessoa = pessoa)
        if apropriacao:
            apropriacao = apropriacao[0]
            return ApropriacaoSerializer(apropriacao).data
        
        return None
    
    def gravar_apropriacao(self, apr, pessoa):
        if apr:
            campos = ('unidade_administrativa', 'centro_custo', 'centro_resultado', 'conta_gerencial', 'natureza_operacao')
            if len([campo for campo in campos if campo in apr]) > 0:
                unidade_administrativa = None
                if 'unidade_administrativa' in apr and apr['unidade_administrativa']:
                    if apr['unidade_administrativa']['id']:
                        unidade_administrativa = UnidadeAdministrativa.objects.get(pk=apr['unidade_administrativa']['id'])
                    del apr['unidade_administrativa']
                
                centro_custo = None
                if 'centro_custo' in apr and apr['centro_custo']:
                    if apr['centro_custo']['id']:
                        centro_custo = CentroCusto.objects.get(pk=apr['centro_custo']['id'])
                    del apr['centro_custo']
                    
                centro_resultado = None
                if 'centro_resultado' in apr and apr['centro_resultado']:
                    if apr['centro_resultado']['id']:
                        centro_resultado = CentroResultado.objects.get(pk=apr['centro_resultado']['id'])
                    del apr['centro_resultado']
                    
                conta_gerencial = None
                if 'conta_gerencial' in apr and apr['conta_gerencial']:
                    if apr['conta_gerencial']['id']:
                        conta_gerencial = ContaGerencial.objects.get(pk=apr['conta_gerencial']['id'])
                    del apr['conta_gerencial']
                    
                natureza_operacao = None
                if 'natureza_operacao' in apr and apr['natureza_operacao']:
                    if apr['natureza_operacao']['id']:
                        natureza_operacao = NaturezaOperacao.objects.get(pk=apr['natureza_operacao']['id'])
                    del apr['natureza_operacao']
                    
                apropriacao = Apropriacao(**apr)
                apropriacao.pessoa = pessoa
                apropriacao.unidade_administrativa = unidade_administrativa
                apropriacao.centro_custo = centro_custo
                apropriacao.centro_resultado = centro_resultado
                apropriacao.conta_gerencial = conta_gerencial
                apropriacao.natureza_operacao = natureza_operacao
                apropriacao.save()
            elif 'id' in apr:
                apropriacao = Apropriacao.objects.get(apr['id'])
                apropriacao.delete()
            
    
    def gravar_pessoa_fisica(self, pf, pessoa):
       
        prestadores = None
        if 'prestadores' in pf:
            prestadores = pf['prestadores']
            del pf['prestadores']
             
        custos_prestador = None
        if 'custos_prestador' in pf:
            custos_prestador = pf['custos_prestador']
            del pf['custos_prestador']
        
        unidade_administrativas = None
        if 'unidade_administrativas' in pf:
            unidade_administrativas = pf['unidade_administrativas']
            del pf['unidade_administrativas']
        
        pessoa_fisica = PessoaFisica(**pf)

        pessoa_fisica.pessoa = pessoa
        pessoa_fisica.data_expedicao = converter_string_para_data(pf['data_expedicao'])
        pessoa_fisica.data_nascimento = converter_string_para_data(pf['data_nascimento'])
        pessoa_fisica.data_emicao_pis = converter_string_para_data(pf['data_emicao_pis'])
        
        pessoa_fisica.save()
        
        self.gravar_prestador(prestadores, pessoa_fisica)
        self.gravar_custo_prestador(custos_prestador, pessoa_fisica)
        self.gravar_unidade_administrativas(unidade_administrativas, pessoa_fisica)
    
    def gravar_unidade_administrativas(self, unidade_administrativas, pessoa_fisica):
        
        unidades_administrativas_related = pessoa_fisica.unidade_administrativas.all()
        if unidades_administrativas_related:
            for r in unidades_administrativas_related:
                pessoa_fisica.unidade_administrativas.remove(r)
            pessoa_fisica.save()
        
        if unidade_administrativas:
            for u in unidade_administrativas:
                if 'id' in u:
                    unidade = UnidadeAdministrativa.objects.get(pk=u['id'])
                    pessoa_fisica.unidade_administrativas.add(unidade)
        
        pessoa_fisica.save()
    
    def gravar_custo_prestador(self, custos_prestador, pessoa_fisica):
        if custos_prestador:
            for custo_prestador_list in custos_prestador:
                if 'remover' not in custo_prestador_list or custo_prestador_list['remover'] == False:
                    custo = CustoPrestador(**custo_prestador_list)
                    custo.pessoa_fisica = pessoa_fisica
                    custo.data_inicio = converter_string_para_data(custo_prestador_list['data_inicio'])
                    if 'data_fim' in custo_prestador_list:
                        custo.data_fim = converter_string_para_data(custo_prestador_list['data_fim'])
                    custo.valor = converter_string_para_float(custo_prestador_list['valor'])
                    custo.save()
                elif 'id' in custo_prestador_list:
                    custo = CustoPrestador.objects.get(pk=custo_prestador_list['id'])
                    custo.delete()
        
    def gravar_pessoa_juridica(self, pj, pessoa):
        
        contatos = None
        if 'contatos' in pj:
            contatos = pj['contatos']
            del pj['contatos']
        
        arquivo = None
        if 'arquivo' in pj:
            arquivo = pj['arquivo']
            del pj['arquivo']
        
        pessoa_juridica = PessoaJuridica(**pj)
        pessoa_juridica.pessoa = pessoa
       
        self.gravar_arquivo(arquivo, pessoa_juridica)
        
        pessoa_juridica.save()
        
        self.gravar_contatos(contatos, pessoa_juridica)
      
    def gravar_arquivo(self, arquivo, pessoa_juridica):
        
        if arquivo:
            if 'remover' not in arquivo or arquivo['remover'] is False:
                
                arquivo = Arquivo(**arquivo)
                pessoa_juridica.arquivo = arquivo
                arquivo.save()
                
            elif 'id' in arquivo:
                arquivo = Arquivo.objects.get(pk=arquivo[id])
                pessoa_juridica.arquivo = None
                pessoa_juridica.save()
                arquivo.delete()
        
    def gravar_contatos(self, contatos, pessoa_juridica):
        if contatos:
            for i in contatos:
                if 'remover' not in i or i['remover'] is False:
                    telefones = None
                    if 'telefones' in i:
                        telefones = i['telefones']
                        del i['telefones']
                        
                    contato = Contato(**i)
                    contato.pessoa_juridica = pessoa_juridica
                    contato.save()
                    
                    self.gravar_telefones_contato(telefones, contato)
                elif 'id' in i:
                    contato = Contato.objects.get(pk=i['id'])
                    contato.delete()
                 
    def gravar_telefones_contato(self, telefones, contato):
        if telefones:
            for i in telefones:
                if 'remover' not in i or i['remover'] is False:
                    telefone = TelefoneContato(**i)
                    telefone.contato = contato
                    telefone.save()
                elif 'id' in i:
                    telefone = TelefoneContato.objects.get(pk=i['id'])
                    telefone.delete()
                
    def gravar_prestador(self, prestadores, pessoa_fisica):
        if prestadores:
            for p in prestadores:
                campos = ('tipo_prestador', 'pessoa_juridica', 'data_exame_admissional', 'data_exame_demissional', 'data_proxima_avaliacao', 'data_ultima_avaliacao', 'data_ultimo_exame_periodico', 'cargo')
                if len([campo for campo in campos if campo in p]) > 0:
                    
                    cargo = None
                    if 'cargo' in p and p['cargo']:
                        if p['cargo']['id']:
                            cargo = Cargo.objects.get(pk=p['cargo']['id'])
                        del p['cargo']
                        
                    usuario = None
                    if 'usuario' in p and p['usuario']:
                        if p['usuario']['id']:
                            usuario = User.objects.get(pk=p['usuario']['id'])
                        del p['usuario']
                    
                    pessoa_juridica = None
                    if 'pessoa_juridica' in p and p['pessoa_juridica']:
                        if p['pessoa_juridica']['id']:
                            pessoa_juridica = PessoaJuridica.objects.get(pk=p['pessoa_juridica']['id'])
                        del p['pessoa_juridica']
                        
                    prestador = Prestador(**p)
                    
                    prestador.pessoa_fisica = pessoa_fisica
                    if 'data_inicio' in p:
                        prestador.data_inicio = converter_string_para_data(p['data_inicio'])
                    if 'data_fim' in p:
                        prestador.data_fim = converter_string_para_data(p['data_fim'])
                    if 'data_contratacao' in p:
                        prestador.data_contratacao = converter_string_para_data(p['data_contratacao'])
                    if 'data_rescisao' in p:
                        prestador.data_rescisao = converter_string_para_data(p['data_rescisao'])
                    if 'data_fim_aditivo' in p:
                        prestador.data_fim_aditivo = converter_string_para_data(p['data_fim_aditivo'])
                    if 'data_exame_admissional' in p:
                        prestador.data_exame_admissional = converter_string_para_data(p['data_exame_admissional'])
                    if 'data_exame_demissional'in p:
                        prestador.data_exame_demissional = converter_string_para_data(p['data_exame_demissional'])
                    if 'data_proxima_avaliacao' in p:
                        prestador.data_proxima_avaliacao = converter_string_para_data(p['data_proxima_avaliacao'])
                    if 'data_ultima_avaliacao' in p:
                        prestador.data_ultima_avaliacao = converter_string_para_data(p['data_ultima_avaliacao'])
                    if 'data_ultimo_exame_periodico' in p:
                        prestador.data_ultimo_exame_periodico = converter_string_para_data(p['data_ultimo_exame_periodico'])
                        
                    prestador.cargo = cargo
                    prestador.usuario = usuario
                    prestador.pessoa_juridica = pessoa_juridica
                    
                    prestador.save();
                    
                elif 'id' in p:
                    prestador = Prestador.objects.get(pk=p['id'])
                    prestador.delete()
        
    def gravar_telefones(self, telefones, pessoa):
        if telefones:
            for i in telefones:
                if 'remover' not in i or i['remover'] is False:
                    telefone = TelefonePessoa(**i)
                    telefone.pessoa = pessoa
                    telefone.save()
                elif 'id' in i:
                    telefone = TelefonePessoa.objects.get(pk=i['id'])
                    telefone.delete()
            
    def gravar_enderecos(self, enderecos, pessoa):
        if enderecos:
            for i in enderecos:
                if 'remover' not in i or i['remover'] is False:
                    endereco = EnderecoPessoa(**i)
                    endereco.pessoa = pessoa
                    endereco.save()
                elif 'id' in i:
                    endereco = EnderecoPessoa.objects.get(pk=i['id'])
                    endereco.delete()     
     
    def gravar_dados_bancarios(self, dados_bancarios, pessoa):
        if dados_bancarios:
            for i in dados_bancarios:
                if 'remover' not in i or i['remover'] is False:
                    dado_bancario = DadosBancariosPessoa(**i)
                    dado_bancario.pessoa = pessoa
                    dado_bancario.save()
                elif 'id' in i:
                    dado_bancario = DadosBancariosPessoa.objects.get(pk=i['id'])
                    dado_bancario.delete()
                
    def delete(self, request, pessoa_id, format=None):
        pessoa = Pessoa.objects.get(pk=pessoa_id)
        pessoa.delete()
        data = self.serializar_pessoa(pessoa)
        return Response(data)
    
    
@api_view(['GET'])
def buscar_pessoas_por_nome(request, texto, format=None):
    pessoas = PessoaFisica.objects.filter(pessoa__nome_razao_social__icontains=texto)
    data = PessoaFisicaComPessoaSerializer(pessoas, many=True).data
    return Response(data)

@api_view(['GET'])
def buscar_gestores(request, format=None):
    pessoas = PessoaFisica.objects.filter(prestador__cargo__gestor=True).order_by('pessoa__nome_razao_social')
    data = PessoaFisicaComPessoaSerializer(pessoas, many=True).data
    return Response(data)

@api_view(['GET'])
def remover_arquivo(request, pessoa_juridica_id, format=None):
    
    pj = PessoaJuridica.objects.get(pk=pessoa_juridica_id)
    
    arquivo = pj.arquivo
    
    pj.arquivo = None
    pj.save()
    
    if arquivo:
        path_arquivo = arquivo.path_arquivo
        os.remove(path_arquivo)
        arquivo.delete()
        
    return Response(ArquivoSerializer(arquivo).data)

@api_view(['POST'])
def upload_arquivo(request, pessoa_juridica_id):    
    
    f = request.FILES['file']

    pj = PessoaJuridica.objects.get(pk=pessoa_juridica_id)
    
    arquivo = pj.arquivo
    
    pj.arquivo = None
    pj.save()
    
    if arquivo:
        path_arquivo = arquivo.path_arquivo
        os.remove(path_arquivo)
        arquivo.delete()
        
    nome_arquivo = f.name
    content_type = f.content_type
    tamanho = f.size
    
    path = criar_arquivo_diretorio(f, pessoa_juridica_id)
    
    arquivo = Arquivo(nome_arquivo = nome_arquivo, 
                      content_type = content_type,tamanho = tamanho, path_arquivo = path )
        
    arquivo.save()
    
    pj.arquivo = arquivo
    pj.save()
    
    return Response(ArquivoSerializer(arquivo).data)

PASTA_ARQUIVOS = importlib.import_module(os.environ['DJANGO_SETTINGS_MODULE']).PASTA_ARQUIVOS

def criar_arquivo_diretorio(f, pessoa_juridica_id):
    
    arquivo = PASTA_ARQUIVOS + pessoa_juridica_id + '/' + f.name
    
    os.makedirs(os.path.dirname(arquivo), exist_ok=True)
    
    with open(arquivo, 'wb+') as destino:
        for chunk in f.chunks():
            destino.write(chunk)
            
    return arquivo

def baixar_arquivo(request, pessoa_juridica_id):
    
    arquivo = Arquivo.objects.filter(pessoajuridica__id = pessoa_juridica_id).order_by('-id')[0]
    
    with open(arquivo.path_arquivo, mode='rb') as arquivo_template:
        response = HttpResponse(arquivo_template, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=' + arquivo.nome_arquivo
        return response
    
@api_view(['GET'])
def buscar_pessoa_juridica_clientes(request):
    pessoas = PessoaJuridica.objects.filter(pessoa__tipo__in ='J', cliente_demanda = True).order_by('pessoa__nome_razao_social')
    data = PessoaJuridicaComPessoaSerializer(pessoas, many=True).data
    return Response(data)
    