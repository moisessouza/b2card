# -*- coding: utf-8 -*-
from io import BytesIO
import zipfile
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from utils.utils import formatar_id, formatar_para_valor_monetario_com_simbolo
from demandas.models import Orcamento, OrcamentoFase, ItemFase, Demanda
import re
import sys

def realizar_replace_docx(demanda_id, template_docx, tipo_proposta):
    
    arquivo_gerado = BytesIO()
    
    demanda = Demanda.objects.get(pk=demanda_id)
    
    id_pad = formatar_id(int(demanda_id))
    
    zin = zipfile.ZipFile (template_docx, 'r')
    zout = zipfile.ZipFile (arquivo_gerado, 'w')
    
    valores = {
        '#iddemanda#': id_pad, 
        '#codigo_no_cliente#': demanda.codigo_demanda,
        '#descricao_da_demanda#': demanda.descricao,
        '#tipoproposta#': 'Técnica' if tipo_proposta == 'T' else 'comercial',
        '#tipo_informacoes#': 'Comerciais' if tipo_proposta == 'T' else 'Orçamentárias',
        '#forma_pagamento#': demanda.forma_pagamento if demanda.forma_pagamento else (demanda.cliente.forma_pagamento if demanda.cliente.forma_pagamento else ''),
        '#particularidade_proposta#': demanda.particularidade_proposta if demanda.particularidade_proposta else (demanda.cliente.particularidade_proposta if demanda.cliente.particularidade_proposta else '')
    }
    
    document_xml = zin.read('word/document.xml').decode()
    variaveis = extrair_variaveis(document_xml)
    
    for i in valores:
        valor = valores[i]
        
        if valor and i in variaveis:
            list = variaveis[i]
            for token in list:
                document_xml = document_xml.replace(token, normalizar_valor(valor))
       
    if '#TABELA#' in variaveis:
        xml_string = gerar_tabela(demanda, tipo_proposta)
        
        list = variaveis['#TABELA#']
        for token in list:
            document_xml = document_xml.replace(token, xml_string)
    
    zout.writestr('word/document.xml',document_xml)
    
    exists = True
    count = 1
    
    list_files = []
    
    while(exists):
        try:
            header = zin.read('word/header{0}.xml'.format(count)).decode()
            list_files.append('word/header{0}.xml'.format(count))
            if header:
                variaveis = extrair_variaveis(header)
                for i in valores:
                    valor = valores[i]
                    if i in variaveis:
                        list = variaveis[i]
                        for token in list:
                            header = header.replace(token, normalizar_valor(valor))
                    
                zout.writestr('word/header{0}.xml'.format(count), header)
            else:
                exists = False    
            count+=1
        except:
            #print (str(sys.exc_info()[0]))
            exists = False
    
    for item in zin.infolist():
        buffer = zin.read(item.filename)
        if (item.filename[-12:] != 'document.xml' and item.filename not in list_files):
            try:
                zout.writestr(item, buffer)
            except:
                pass
    
    zin.close()
    zout.close()
    
    return arquivo_gerado

def normalizar_valor(valor):
    
    if valor and '\n' in valor:
        novo_valor = ''
        split = valor.split('\n')
        
        for s in split:
            novo_valor += """<w:p w:rsidR="00367E05" w:rsidRDefault="00F1681A" w:rsidP="00613C71">
                                 <w:pPr>
                                    <w:spacing w:line="360" w:lineRule="auto" />
                                    <w:jc w:val="both" />
                                    <w:rPr>
                                       <w:rFonts w:asciiTheme="minorHAnsi" w:hAnsiTheme="minorHAnsi" w:cs="Arial" />
                                       <w:color w:val="767171" />
                                    </w:rPr>
                                 </w:pPr>
                                 <w:r>
                                    <w:rPr>
                                       <w:rFonts w:asciiTheme="minorHAnsi" w:hAnsiTheme="minorHAnsi" w:cs="Arial" />
                                       <w:color w:val="767171" />
                                    </w:rPr>
                                    <w:t xml:space="preserve">""" + s + """</w:t>
                                 </w:r>
                              </w:p>"""
        valor = novo_valor
        
    return valor

def extrair_variaveis (arquivo):

    variaveis = {}

    contem_token = True

    while contem_token:
    
        if '#' not in arquivo:
            contem_token = False
        else:
            inicio = arquivo.index('#') + 1
            arquivo = arquivo[inicio:]
            if '#' in arquivo:
                fim = arquivo.index('#')
                variavel = arquivo[:fim]
                
                token = '#' + variavel + '#'
                
                variavel = regularizar_variavel(variavel)
                if variavel in ['iddemanda', 'codigo_no_cliente', 'descricao_da_demanda', 'tipoproposta', 'tipo_informacoes', 'TABELA', 'forma_pagamento', 'particularidade_proposta']:
                    variavel = '#' + variavel + '#'
                    if variavel in variaveis:
                        variaveis[variavel].append(token)
                    else:
                        variaveis[variavel] = [token]
                    if len(arquivo) > fim:
                        arquivo = arquivo[(fim + 1):]
            else:
                contem_token = False
    
    return variaveis
    
def regularizar_variavel(variavel):
    
    variavel = re.sub('<\w*:\w*\s*[\w|:|=|\"]*\s*[\w|:|=|\"]*\s*[\w|:|=|\"|/]*\s*[\w|:|=|\"|/]*\s*[\w|:|=|\"|/]*\s*[\w|:|=|\"|/]*>', '', variavel)
    variavel = re.sub('</\w*:(\w*)>', '', variavel)
    
    return variavel
    
def gerar_tabela(demanda, tipo_proposta):

    orcamento = Orcamento.objects.get(demanda__id = demanda.id)
    
    orcamento_fases = []
    orcamento_fases.extend(OrcamentoFase.objects.filter(orcamento = orcamento))
    
    demandas_complementares = demanda.demandas_complementares.all()
    
    if demandas_complementares:
        for dc in demandas_complementares:
            orcamento_fases.extend(OrcamentoFase.objects.filter(orcamento__demanda = dc))
    
    linhas = [];
    
    for orcamento_fase in orcamento_fases:
        
        item_fases = ItemFase.objects.filter(orcamento_fase = orcamento_fase)
        
        eh_primeiro = True
        
        for i in item_fases:
            linha = []
            if eh_primeiro:
                linha.append(orcamento_fase.fase.descricao)
                linha.append(i.valor_hora.descricao)
                if tipo_proposta == 'C':
                    linha.append(formatar_para_valor_monetario_com_simbolo(i.valor_selecionado))
                linha.append(int(round(i.quantidade_horas)))
                linha.append(int(round(buscar_total_horas_orcamento_fase(item_fases))))
                if tipo_proposta == 'C':
                    linha.append(formatar_para_valor_monetario_com_simbolo(orcamento_fase.valor_total))
                linha.append('0')
                eh_primeiro = False
            else:
                linha.append(None)
                linha.append(i.valor_hora.descricao)
                if tipo_proposta == 'C':
                    linha.append(formatar_para_valor_monetario_com_simbolo(i.valor_selecionado))
                linha.append(int(round(i.quantidade_horas)))
                linha.append(None)
                linha.append(None)
                linha.append(None)
            linhas.append(linha)

    tbl = criar_tabela()
    
    cab = adicionar_cabecalho(tbl)
    
    adicionar_coluna_cabecalho(cab, ["Fase"])
    adicionar_coluna_cabecalho(cab, ["Perfil"])
    if tipo_proposta == 'C':
        adicionar_coluna_cabecalho(cab, ["Vlr Hora"])
    adicionar_coluna_cabecalho(cab, ["Esforço", "(Horas)"])
    adicionar_coluna_cabecalho(cab, ["Esforço", "(Horas P/Fase)"])
    if tipo_proposta == 'C':
        adicionar_coluna_cabecalho(cab, ["Valor (P/Fase)"])
    adicionar_coluna_cabecalho(cab, ["Prazo", "(Dias)"])
    
    for l in linhas:
        adicionar_linha_tabela(tbl, l)
        
    adicionar_rodape(tbl, demanda, orcamento, tipo_proposta)
    
    xml_string = tostring(tbl)
    xml_string = xml_string.decode()
    
    return xml_string

def adicionar_rodape(tbl, demanda, orcamento, tipo_proposta):
    
    tr = SubElement(tbl, 'w:tr', attrib = {'w:rsidR': "00492691", 'w:rsidTr':"00492691"})
    trPr = SubElement(tr, 'w:trPr')
    SubElement(trPr, 'w:trHeight', attrib = {'w:val':"270"})
    
    def buscar_total_horas_orcamento(demanda, orcamento):
        total_horas = 0
        total_preco = 0
        
        orcamento_fases = []
        orcamento_fases.extend(OrcamentoFase.objects.filter(orcamento = orcamento))
        
        demandas_complementares = demanda.demandas_complementares.all()
    
        if demandas_complementares:
            for dc in demandas_complementares:
                orcamento_fases.extend(OrcamentoFase.objects.filter(orcamento__demanda = dc))
        
        
        for of in orcamento_fases:
            item_fases = ItemFase.objects.filter(orcamento_fase = of)
            valor = buscar_total_horas_orcamento_fase(item_fases)
            total_horas += valor
            total_preco += of.valor_total
            
        return total_horas, total_preco
        
    adicionar_coluna_rodape(tr, 'Total')
    adicionar_coluna_rodape(tr, None)
    adicionar_coluna_rodape(tr, None)
    if tipo_proposta == 'C':
        adicionar_coluna_rodape(tr, None)
    
    total_horas, total_preco = buscar_total_horas_orcamento(demanda, orcamento)
    
    adicionar_coluna_rodape(tr, int(round(total_horas)))
    if tipo_proposta == 'C':
        adicionar_coluna_rodape(tr, formatar_para_valor_monetario_com_simbolo(total_preco))
    adicionar_coluna_rodape(tr, None)
    

def adicionar_coluna_rodape(tr, coluna):
    
    tc = SubElement(tr, 'w:tc')
    
    tcPr = SubElement(tc, 'w:tcPr')
    SubElement(tcPr, 'w:tcW', attrib={'w:w':"2380", 'w:type':"dxa"})
    #SubElement(tcPr, 'w:vMerge', attrib={'w:val':"restart"})
    tcBorders = SubElement(tcPr, 'w:tcBorders')
    SubElement(tcBorders, 'w:top', attrib = { 'w:val':"nil"})
    SubElement(tcBorders, 'w:left', attrib = {'w:val':"single", 'w:sz':"8", 'w:space':"0", 'w:color':"auto"})
    SubElement(tcBorders, 'w:bottom', attrib = {'w:val':"single", 'w:sz':"8", 'w:space':"0", 'w:color':"auto"})
    SubElement(tcBorders, 'w:right', attrib = {'w:val':"single", 'w:sz':"8", 'w:space':"0", 'w:color':"auto"})
    SubElement(tcPr,'w:shd', attrib= { 'w:val':"clear", 'w:color':"000000", 'w:fill':"808080"})
    SubElement(tcPr, 'w:vAlign', attrib = {'w:val':"center"}) 
    SubElement(tcPr, 'w:hideMark')
    
    if coluna:
    
        p = SubElement(tc, 'w:p', attrib= { 'w:rsidR':"002C6851", 'w:rsidRDefault':"002C6851"})
        pPr = SubElement(p, 'w:pPr')
        SubElement(pPr, 'w:jc', attrib={'w:val':"center"})
        rPr = SubElement(pPr, 'w:rPr')
        SubElement(rPr, 'w:rFonts',  attrib ={ 'w:ascii':"Calibri", 'w:hAnsi':"Calibri", 'w:cs':"Arial" })
        SubElement(rPr, 'w:b')
        SubElement(rPr, 'w:bCs')
        SubElement(rPr, 'w:color', attrib= {'w:val':"000000"})
        SubElement(rPr, 'w:sz', attrib= {'w:val':"20"})
        SubElement(rPr, 'w:szCs', attrib= {'w:val':"20"})
        
        r = SubElement(p, 'w:r')
        pPr = SubElement(r, 'w:pPr')
        SubElement(pPr, 'w:jc', attrib = {'w:val':"center"})
        rPr = SubElement(pPr, 'w:rPr')
        SubElement(rPr, 'w:rFonts', attrib = {'w:ascii': "Calibri", 'w:hAnsi':"Calibri", 'w:cs':"Arial"})
        SubElement(rPr, 'w:color', attrib = {'w:val':"000000"})
        SubElement(rPr, 'w:sz', attrib = {'w:val':"20"})
        SubElement(rPr, 'w:szCs', attrib = {'w:val':"20"})
        
        t = SubElement(r, 'w:t')
        t.text = str(coluna)
    else:
        tcPr = SubElement(tc, 'w:tcPr')
        SubElement(tcPr, 'w:tcW', attrib = {'w:w':"2380", 'w:type':"dxa"})
        tcBorders = SubElement(tcPr, 'w:tcBorders')
        SubElement(tcBorders, 'w:top', attrib = {'w:val': 'nil'})
        SubElement(tcBorders, 'w:left', attrib = {'w:val': "single",'w:sz':"8", 'w:space':"0", 'w:color':"auto"})
        SubElement(tcBorders, 'w:bottom', attrib = {'w:val':"single", 'w:sz':"8", 'w:space':"0", 'w:color':"000000"})
        SubElement(tcBorders, 'w:right', attrib = {'w:val':"single", 'w:sz':"8", 'w:space':"0", 'w:color':"auto"})
        SubElement(tcPr, 'w:vAlign', attrib = {'w:val':"center"})
        SubElement(tcPr, 'w:hideMark')
        
        p = SubElement(tc, 'w:p', attrib = { 'w:rsidR':"00492691", 'w:rsidRDefault':"00492691"})
        pPr = SubElement(p, 'w:pPr')
        rPr = SubElement(pPr, 'w:rPr')
        SubElement(rPr, 'w:rFonts', attrib = {'w:ascii': "Calibri", 'w:hAnsi':"Calibri", 'w:cs':"Arial"})
        SubElement(rPr, 'w:color', attrib = {'w:val':"000000"})
        SubElement(rPr, 'w:sz', attrib = {'w:val':"20"})
        SubElement(rPr, 'w:szCs', attrib = {'w:val':"20"})
    
def buscar_total_horas_orcamento_fase(item_fases):
    soma = 0;
    
    for i in item_fases:
        soma += i.quantidade_horas
    
    return soma

def criar_tabela():
    
    ET.register_namespace('w', 'http://schemas.openxmlformats.org/wordprocessingml/2006/main')
    ET.register_namespace('m', 'http://schemas.openxmlformats.org/officeDocument/2006/math')
    ET.register_namespace('mc', 'http://schemas.openxmlformats.org/markup-compatibility/2006')
    ET.register_namespace('o', 'urn:schemas-microsoft-com:office:office')
    ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')
    ET.register_namespace('v', 'urn:schemas-microsoft-com:vml')
    ET.register_namespace('w10', 'urn:schemas-microsoft-com:office:word')
    ET.register_namespace('w14', 'http://schemas.microsoft.com/office/word/2010/wordml')
    ET.register_namespace('w15', 'http://schemas.microsoft.com/office/word/2012/wordml')
    ET.register_namespace('wne', 'http://schemas.microsoft.com/office/word/2006/wordml')
    ET.register_namespace('wp', 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing')
    ET.register_namespace('wp14', 'http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing')
    ET.register_namespace('wpc', 'http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas')
    ET.register_namespace('wpg', 'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup')
    ET.register_namespace('wpi', 'http://schemas.microsoft.com/office/word/2010/wordprocessingInk')
    ET.register_namespace('wps', 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape')
    
    tbl = Element('w:tbl')
    
    tblPr = SubElement(tbl, 'w:tblPr')
    
    SubElement(tblPr, 'w:tblW', attrib = {'w:w':'5300', 'w:type':'pct'})
    tblCellMar = SubElement(tblPr, 'w:tblCellMar')
    
    SubElement(tblCellMar, 'w:left', attrib = {'w:w' : "70", 'w:type' : "dxa"})
    SubElement(tblCellMar, 'w:right', attrib = {'w:w' : "70", 'w:type' : "dxa"})
    
    SubElement(tblPr, 'w:tblLook', attrib = {'w:val' : "04A0", 'w:firstRow':"1", 'w:lastRow':"0", 'w:firstColumn':"1", 'w:lastColumn':"0", 'w:noHBand':"0", 'w:noVBand':"1"})
    
    #tblGrid = SubElement(tbl, "w:tblGrid")
    
    #SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"1834"})
    #SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"2560"})
    #SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"955"})
    #SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"1001"})
    #SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"1432"})
    #SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"1141"})
    #SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"696"})    
    
    return tbl

def adicionar_cabecalho(tbl):
    
    tr = SubElement(tbl, 'w:tr', attrib={ 'w:rsidR':"00CD4609", 'w:rsidTr':"00CD4609" })
    trPr = SubElement(tr, 'w:trPr')
    SubElement(trPr, 'w:trHeight', attrib = {'w:val':'255'})
    
    return tr
    
    
def adicionar_coluna_cabecalho(tr, linhas_na_coluna):
    
    tc = SubElement(tr, 'w:tc')
    tcPr = SubElement(tc, 'w:tcPr')
    SubElement(tcPr, 'w:tcW', attrib={'w:w':"955", 'w:type':"dxa"})
    SubElement(tcPr, 'w:vMerge', attrib={'w:val':"restart"})
    tcBorders = SubElement(tcPr, 'w:tcBorders')
    SubElement(tcBorders, 'w:top', attrib = {'w:val':"single", 'w:sz':"8", 'w:space':"0", 'w:color':"auto"})
    SubElement(tcBorders, 'w:left', attrib = {'w:val':"single", 'w:sz':"8", 'w:space':"0", 'w:color':"auto"})
    SubElement(tcBorders, 'w:bottom', attrib = {'w:val':"single", 'w:sz':"8", 'w:space':"0", 'w:color':"auto"})
    SubElement(tcBorders, 'w:right', attrib = {'w:val':"single", 'w:sz':"8", 'w:space':"0", 'w:color':"auto"})
    SubElement(tcPr,'w:shd', attrib= { 'w:val':"clear", 'w:color':"000000", 'w:fill':"808080"})
    SubElement(tcPr, 'w:vAlign', attrib = {'w:val':"center"}) 
    SubElement(tcPr, 'w:hideMark')
    p = SubElement(tc, 'w:p', attrib= { 'w:rsidR':"002C6851", 'w:rsidRDefault':"002C6851"})
    pPr = SubElement(p, 'w:pPr')
    SubElement(pPr, 'w:jc', attrib={'w:val':"center"})
    rPr = SubElement(pPr, 'w:rPr')
    SubElement(rPr, 'w:rFonts',  attrib ={ 'w:ascii':"Calibri", 'w:hAnsi':"Calibri", 'w:cs':"Arial" })
    SubElement(rPr, 'w:b')
    SubElement(rPr, 'w:bCs')
    SubElement(rPr, 'w:color', attrib= {'w:val':"000000"})
    SubElement(rPr, 'w:sz', attrib= {'w:val':"20"})
    SubElement(rPr, 'w:szCs', attrib= {'w:val':"20"})
    
    primeira_linha = True
    for linha in linhas_na_coluna:
        r = SubElement(p, 'w:r')
        rPr = SubElement(r, 'w:rPr')
        SubElement(rPr, 'w:rFonts',  attrib ={ 'w:ascii':"Calibri", 'w:hAnsi':"Calibri", 'w:cs':"Arial" })
        SubElement(rPr, 'w:b')
        SubElement(rPr, 'w:bCs')
        SubElement(rPr, 'w:color', attrib= {'w:val':"000000"})
        SubElement(rPr, 'w:sz', attrib= {'w:val':"20"})
        SubElement(rPr, 'w:szCs', attrib= {'w:val':"20"})
        if primeira_linha:
            primeira_linha = False
        else:
            SubElement(r, 'w:br')
            
        t = SubElement(r, 'w:t', attrib = {'xml:space':"preserve"})
        t.text = linha
        
def adicionar_linha_tabela(tbl, colunas):
    
    tr = SubElement(tbl, 'w:tr', attrib = {'w:rsidR': "00492691", 'w:rsidTr':"00492691"})
    trPr = SubElement(tr, 'w:trPr')
    SubElement(trPr, 'w:trHeight', attrib = {'w:val':"255"})
    
    if colunas:
        for c in colunas:
            adicionar_coluna(tr, c)
            
def adicionar_coluna(tr, coluna):
    
    if coluna:
        tc = SubElement(tr, 'w:tc')
        tcPr = SubElement(tc, 'w:tcPr')
        SubElement(tcPr, 'w:tcW', attrib = {'w:w':"2380", 'w:type':"dxa"})
        SubElement(tcPr, 'w:vMerge', attrib = {'w:val':"restart"})
        tcBorders = SubElement(tcPr, 'w:tcBorders')
        SubElement(tcBorders, 'w:top', attrib = {'w:val': 'nil'})
        SubElement(tcBorders, 'w:left', attrib = {'w:val': "single",'w:sz':"8", 'w:space':"0", 'w:color':"auto"})
        SubElement(tcBorders, 'w:bottom', attrib = {'w:val':"single", 'w:sz':"8", 'w:space':"0", 'w:color':"000000"})
        SubElement(tcBorders, 'w:right', attrib = {'w:val':"single", 'w:sz':"8", 'w:space':"0", 'w:color':"auto"})
        SubElement(tcPr, 'w:shd', attrib = {'w:val':"clear", 'w:color':"000000", 'w:fill':"D9D9D9"})
        SubElement(tcPr, 'w:vAlign', attrib = {'w:val':"center"})
        SubElement(tcPr, 'w:hideMark')
        
        p = SubElement(tc, 'w:p', attrib = { 'w:rsidR':"00492691", 'w:rsidRDefault':"00492691"})
        pPr = SubElement(p, 'w:pPr')
        SubElement(pPr, 'w:jc', attrib = {'w:val':"center"})
        rPr = SubElement(pPr, 'w:rPr')
        SubElement(rPr, 'w:rFonts', attrib = {'w:ascii': "Calibri", 'w:hAnsi':"Calibri", 'w:cs':"Arial"})
        SubElement(rPr, 'w:color', attrib = {'w:val':"000000"})
        SubElement(rPr, 'w:sz', attrib = {'w:val':"20"})
        SubElement(rPr, 'w:szCs', attrib = {'w:val':"20"})
        
        r = SubElement(p, 'w:r')
        pPr = SubElement(r, 'w:pPr')
        SubElement(pPr, 'w:jc', attrib = {'w:val':"center"})
        rPr = SubElement(pPr, 'w:rPr')
        SubElement(rPr, 'w:rFonts', attrib = {'w:ascii': "Calibri", 'w:hAnsi':"Calibri", 'w:cs':"Arial"})
        SubElement(rPr, 'w:color', attrib = {'w:val':"000000"})
        SubElement(rPr, 'w:sz', attrib = {'w:val':"20"})
        SubElement(rPr, 'w:szCs', attrib = {'w:val':"20"})
        
        t = SubElement(r, 'w:t')
        t.text = str(coluna)
        
    else:
        tc = SubElement(tr, 'w:tc')
        tcPr = SubElement(tc, 'w:tcPr')
        SubElement(tcPr, 'w:tcW', attrib = {'w:w':"2380", 'w:type':"dxa"})
        SubElement(tcPr, 'w:vMerge')
        tcBorders = SubElement(tcPr, 'w:tcBorders')
        SubElement(tcBorders, 'w:top', attrib = {'w:val': 'nil'})
        SubElement(tcBorders, 'w:left', attrib = {'w:val': "single",'w:sz':"8", 'w:space':"0", 'w:color':"auto"})
        SubElement(tcBorders, 'w:bottom', attrib = {'w:val':"single", 'w:sz':"8", 'w:space':"0", 'w:color':"000000"})
        SubElement(tcBorders, 'w:right', attrib = {'w:val':"single", 'w:sz':"8", 'w:space':"0", 'w:color':"auto"})
        SubElement(tcPr, 'w:vAlign', attrib = {'w:val':"center"})
        SubElement(tcPr, 'w:hideMark')
        
        p = SubElement(tc, 'w:p', attrib = { 'w:rsidR':"00492691", 'w:rsidRDefault':"00492691"})
        pPr = SubElement(p, 'w:pPr')
        rPr = SubElement(pPr, 'w:rPr')
        SubElement(rPr, 'w:rFonts', attrib = {'w:ascii': "Calibri", 'w:hAnsi':"Calibri", 'w:cs':"Arial"})
        SubElement(rPr, 'w:color', attrib = {'w:val':"000000"})
        SubElement(rPr, 'w:sz', attrib = {'w:val':"20"})
        SubElement(rPr, 'w:szCs', attrib = {'w:val':"20"})
        
        
        
def gerar_arquivo_aprovacao(arquivo_docx, parcela_fase):
    
    tbl = criar_tabela()
    
    tr = adicionar_cabecalho(tbl)
    
    adicionar_coluna_cabecalho(tr, ["Demanda"])
    adicionar_coluna_cabecalho(tr, ["Fase"])
    adicionar_coluna_cabecalho(tr, ["Perfil"])
    adicionar_coluna_cabecalho(tr, ["Qtd", "HH", "Contratada"])
    adicionar_coluna_cabecalho(tr, ["Qtd", "HH", "Já" ,"Faturadas"])
    adicionar_coluna_cabecalho(tr, ["Saldo", "HH", "a", "Faturar"])
    adicionar_coluna_cabecalho(tr, ["Horas", "a", "Faturar"])
    adicionar_coluna_cabecalho(tr, ["Valor/HH"])
    adicionar_coluna_cabecalho(tr, ["Valor", "a", "faturar"])
    
    total_horas_contratadas = 0
    total_horas_ja_faturadas = 0
    total_horas_a_faturar = 0
    total_saldo_a_faturar = 0
    total_valor_a_faturar = 0
    
    for m in parcela_fase:
        
        nome_demanda = m['parcela__demanda__nome_demanda']
        codigo_demanda = m['parcela__demanda__codigo_demanda']
        fase_descricao = m['parcela__parcelafase__fase__fase__descricao']
        valor_hora_descricao = m['parcela__parcelafase__medicao__valor_hora__descricao'] 
        horas_contratadas = m['horas_contratadas']
        horas_ja_faturadas = m['horas_ja_faturadas']
        saldo_a_faturar = m['saldo_a_faturar']
        valor_por_hora = m['valor_por_hora']
        
        total_horas_contratadas += horas_contratadas
        total_horas_ja_faturadas += horas_ja_faturadas if horas_ja_faturadas else 0
        total_saldo_a_faturar += saldo_a_faturar
        
        
        valor_por_hora = formatar_para_valor_monetario_com_simbolo(valor_por_hora)
        
        horas_a_faturar = m['horas_a_faturar'] 
        valor_a_faturar = m['valor_a_faturar']
        
        total_horas_a_faturar += horas_a_faturar
        total_valor_a_faturar += valor_a_faturar
        
        valor_a_faturar = formatar_para_valor_monetario_com_simbolo(valor_a_faturar)
        
        adicionar_linha_tabela(tbl, [codigo_demanda + ' - ' + nome_demanda, fase_descricao, 
                                     valor_hora_descricao, horas_contratadas, horas_ja_faturadas if horas_ja_faturadas else '0', saldo_a_faturar, horas_a_faturar, valor_por_hora, valor_a_faturar])
        
    
    
    tr = SubElement(tbl, 'w:tr', attrib = {'w:rsidR': "00492691", 'w:rsidTr':"00492691"})
    trPr = SubElement(tr, 'w:trPr')
    SubElement(trPr, 'w:trHeight', attrib = {'w:val':"270"})
    
    adicionar_coluna_rodape(tr, "Total")
    adicionar_coluna_rodape(tr, None)
    adicionar_coluna_rodape(tr, None)
    adicionar_coluna_rodape(tr, total_horas_contratadas)
    adicionar_coluna_rodape(tr, total_horas_ja_faturadas)
    adicionar_coluna_rodape(tr, total_saldo_a_faturar)
    adicionar_coluna_rodape(tr, round(total_horas_a_faturar, 2))
    adicionar_coluna_rodape(tr, None)
    adicionar_coluna_rodape(tr, total_valor_a_faturar)
    
    arquivo_gerado = BytesIO()
    
    zin = zipfile.ZipFile (arquivo_docx, 'r')
    zout = zipfile.ZipFile (arquivo_gerado, 'w')
    
    document_xml = zin.read('word/document.xml').decode()
    variaveis = extrair_variaveis(document_xml)
    
    xml_string = tostring(tbl)
    xml_string = xml_string.decode()
       
    if '#TABELA#' in variaveis:
        list = variaveis['#TABELA#']
        for token in list:
            document_xml = document_xml.replace(token, xml_string)
    
    zout.writestr('word/document.xml',document_xml)
    
    for item in zin.infolist():
        buffer = zin.read(item.filename)
        if (item.filename[-12:] != 'document.xml'):
            try:
                zout.writestr(item, buffer)
            except:
                pass
    
    zin.close()
    zout.close()
    
    return arquivo_gerado
    