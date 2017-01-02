from django.shortcuts import render
from cadastros.models import TipoHora, CentroCusto, Pessoa, TelefonePessoa,\
    EnderecoPessoa, DadosBancariosPessoa, PessoaFisica, Prestador,\
    PessoaJuridica
from cadastros import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.utils import converter_string_para_data, formatar_data
from cadastros.serializers_pessoa import PessoaSerializer,\
    EnderecoPessoaSerializer, TelefonePessoaSerializer,\
    DadosBancariosPessoaSerializer, PessoaFisicaSerializer, PrestadorSerializer,\
    PessoaJuridicaSerializer

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
        pessoas = Pessoa.objects.all()
        data = PessoaSerializer(pessoas, many=True).data
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
            
        if 'data_fim_aditivo' in data and data['data_fim_aditivo']:
            data['data_fim_aditivo'] = converter_string_para_data(data['data_fim_aditivo'])
            
        if 'data_renegociacao_valor' in data and data['data_renegociacao_valor']:
            data['data_renegociacao_valor'] = converter_string_para_data(data['data_renegociacao_valor'])
        
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
            
        prestador = None
        if 'prestador' in data:
            prestador = data['prestador']
            del data['prestador']
            
        pessoa = Pessoa(**data)
        pessoa.centro_custo = centro_custo
        pessoa.save()
        
        self.gravar_telefones(telefones, pessoa)
        self.gravar_enderecos(enderecos, pessoa)
        self.gravar_dados_bancarios(dados_bancarios, pessoa)
        
        if data['tipo'] == 'F':
            self.gravar_pessoa_fisica(pessoa_fisica, pessoa)
        
        if data['tipo'] == 'J':
            self.gravar_pessoa_juridica(pessoa_juridica, pessoa)
             
        data = self.serializar_pessoa(pessoa)
        
        return Response(data);
    
    def serializar_pessoa(self, pessoa):
        
        data = PessoaSerializer(pessoa).data
        
        data['data_contratacao'] = formatar_data(pessoa.data_contratacao)
        data['data_rescisao'] =  formatar_data(pessoa.data_rescisao)
        data['data_fim_aditivo'] = formatar_data(pessoa.data_fim_aditivo)
        data['data_renegociacao_valor'] = formatar_data(pessoa.data_renegociacao_valor)
        
        data['enderecos'] = self.serializar_enderecos(pessoa)
        data['telefones'] = self.serializar_telefones(pessoa)
        data['dados_bancarios'] = self.serializar_dados_bancarios(pessoa)
        data['pessoa_fisica'] = self.serializar_pessoa_fisica(pessoa)
        data['pessoa_juridica'] = self.serializar_pessoa_juridica(pessoa)
        
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
            data['prestador'] = self.serializar_prestador(pessoa_fisica[0])
            return data
        
        return None
    
    def serializar_pessoa_juridica(self, pessoa):
        pessoa_juridica = PessoaJuridica.objects.filter(pessoa = pessoa)
        if pessoa_juridica:
            data = PessoaJuridicaSerializer(pessoa_juridica[0]).data
            return data
        
        return None
    
    def serializar_prestador(self, pessoa_fisica):
        prestador = Prestador.objects.filter(pessoa_fisica = pessoa_fisica)
        if prestador:
            return PrestadorSerializer(prestador[0]).data
        
        return None
    
    def gravar_pessoa_fisica(self, pf, pessoa):
       
        prestador = None
        if 'prestador' in pf:
            prestador = pf['prestador']
            del pf['prestador']
             
        pessoa_fisica = PessoaFisica(**pf)

        pessoa_fisica.pessoa = pessoa
        pessoa_fisica.data_expedicao = converter_string_para_data(pf['data_expedicao'])
        pessoa_fisica.data_nascimento = converter_string_para_data(pf['data_expedicao'])
        pessoa_fisica.data_emicao_pis = converter_string_para_data(pf['data_emicao_pis'])
        
        self.gravar_prestador(prestador, pessoa_fisica)
        
        pessoa_fisica.save()
    
    def gravar_pessoa_juridica(self, pj, pessoa):
        pessoa_juridica = PessoaJuridica(**pj)
        pessoa_juridica.pessoa = pessoa
        pessoa_juridica.save()
      
    def gravar_prestador(self, p, pessoa_fisica):
        if p:
            campos = ('tipo_prestador', 'data_exame_admissional', 'data_exame_demissional', 'data_proxima_avaliacao', 'data_ultima_avaliacao', 'data_ultimo_exame_periodico')
            if len([campo for campo in campos if campo in p]) > 0:
                
                prestador = Prestador(**p)
                
                prestador.pessoa_fisica = pessoa_fisica
                prestador.data_exame_admissional = converter_string_para_data(p['data_exame_admissional'])
                prestador.data_exame_demissional = converter_string_para_data(p['data_exame_demissional'])
                prestador.data_proxima_avaliacao = converter_string_para_data(p['data_proxima_avaliacao'])
                prestador.data_ultima_avaliacao = converter_string_para_data(p['data_ultima_avaliacao'])
                prestador.data_ultimo_exame_periodico = converter_string_para_data(p['data_ultimo_exame_periodico'])
                
            elif 'id' in p:
                prestador = Prestador.objects.get(pk=p['id'])
                prestador.delete()
    
    def gravar_telefones(self, telefones, pessoa):
        
        for i in telefones:
            if 'remover' not in i or i['remover'] is False:
                telefone = TelefonePessoa(**i)
                telefone.pessoa = pessoa
                telefone.save()
            elif 'id' in i:
                telefone = TelefonePessoa.objects.get(pk=i['id'])
                telefone.delete()
            
    def gravar_enderecos(self, enderecos, pessoa):
        for i in enderecos:
            if 'remover' not in i or i['remover'] is False:
                endereco = EnderecoPessoa(**i)
                endereco.pessoa = pessoa
                endereco.save()
            elif 'id' in i:
                endereco = EnderecoPessoa.objects.get(pk=i['id'])
                endereco.delete()     
     
    def gravar_dados_bancarios(self, dados_bancarios, pessoa):
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
