# -*- coding: utf-8 -*-
from _io import BytesIO, TextIOWrapper, StringIO
import zipfile
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment, tostring

def realizar_replace_docx(arquivo_docx):
    
    arquivo_media = 'media.docx'
    
    zin = zipfile.ZipFile (arquivo_docx, 'r')
    zout = zipfile.ZipFile (arquivo_media, 'w')
    
    document_xml = zin.read('word/document.xml').decode()
    document_xml = document_xml.replace('###CODIGODEMANDA###', 'realizou o replace')
    
    zout.writestr('word/document.xml',document_xml)
    
    exists = True
    count = 1
    
    list_files = []
    
    while(exists):
        try:
            header = zin.read('word/header{0}.xml'.format(count)).decode()
            list_files.append('word/header{0}.xml'.format(count))
            if header:
                header = header.replace('###CODIGODEMANDA###', 'fez no cabecalho')
                zout.writestr('word/header{0}.xml'.format(count), header)
            else:
                exists = False    
            count+=1
        except:
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
    
    return arquivo_media

def criar_tabela_xml(arquivo_docx):
    
    arquivo_gerado = 'demo4.docx'
    
    zin = zipfile.ZipFile (arquivo_docx, 'r')
    document_xml = zin.read('word/document.xml').decode()
    
    namespaces = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
   'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
   'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
   'o': 'urn:schemas-microsoft-com:office:office',
   'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
   'v': 'urn:schemas-microsoft-com:vml',
   'w10': 'urn:schemas-microsoft-com:office:word',
   'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
   'w15': 'http://schemas.microsoft.com/office/word/2012/wordml',
   'wne': 'http://schemas.microsoft.com/office/word/2006/wordml',
   'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
   'wp14': 'http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing',
   'wpc': 'http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas',
   'wpg': 'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup',
   'wpi': 'http://schemas.microsoft.com/office/word/2010/wordprocessingInk',
   'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape'}
    
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
    
    tbl = criar_tabela()
    xml_string = tostring(tbl)
    xml_string = xml_string.decode()
    
    document_xml = document_xml.replace('###TABELA###', xml_string)
    zout = zipfile.ZipFile (arquivo_gerado, 'w')
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
    
    print (xml_string)
  
def criar_tabela():
    
    tbl = Element('w:tbl')
    
    tblPr = SubElement(tbl, 'w:tblPr')
    
    SubElement(tblPr, 'w:tblW', attrib = {'w:w':'5000', 'w:type':'pct'})
    tblCellMar = SubElement(tblPr, 'w:tblCellMar')
    
    SubElement(tblCellMar, 'w:left', attrib = {'w:w' : "70", 'w:type' : "dxa"})
    SubElement(tblCellMar, 'w:right', attrib = {'w:w' : "70", 'w:type' : "dxa"})
    
    SubElement(tblPr, 'w:tblLook', attrib = {'w:val' : "04A0", 'w:firstRow':"1", 'w:lastRow':"0", 'w:firstColumn':"1", 'w:lastColumn':"0", 'w:noHBand':"0", 'w:noVBand':"1"})
    
    tblGrid = SubElement(tbl, "w:tblGrid")
    
    SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"1834"})
    SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"2560"})
    SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"955"})
    SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"1001"})
    SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"1432"})
    SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"1141"})
    SubElement(tblGrid, 'w:gridCol', attrib = {'w:w':"696"})    
    
    adicionar_cabecalho(tbl)
    
    return tbl

def adicionar_cabecalho(tbl):
    
    tr = SubElement(tbl, 'w:tr', attrib={ 'w:rsidR':"00CD4609", 'w:rsidTr':"00CD4609" })
    trPr = SubElement(tr, 'w:trPr')
    SubElement(trPr, 'w:trHeight', attrib = {'w:val':'255'})
    
    adicionar_coluna_cabecalho(tr, ["Fase"])
    adicionar_coluna_cabecalho(tr, ["Perfil"])
    adicionar_coluna_cabecalho(tr, ["Vlr Hora"])
    adicionar_coluna_cabecalho(tr, ["Esforço", "(Horas)"])
    adicionar_coluna_cabecalho(tr, ["Esforço", "(Horas P/Fase)"])
    adicionar_coluna_cabecalho(tr, ["Valor", "(P/Perfil)"])
    adicionar_coluna_cabecalho(tr, ["Prazo", "(Dias)"])
    
    
def adicionar_coluna_cabecalho(tr, linhas):
    
    tc = SubElement(tr, 'w:tc')
    tcPr = SubElement(tc, 'w:tcPr')
    SubElement(tcPr, 'w:tcW', attrib={'w:w':"955", 'w:type':"pct"})
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
    for linha in linhas:
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
        
        
criar_tabela_xml(realizar_replace_docx('proposta_tecnica.docx'))