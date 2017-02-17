from datetime import datetime
import locale
import re

def formatar_data(data):
    if data is not None:
        iso = data.isoformat()
        tokens = iso.strip()
        tokens = iso.split('-')
        return "%s/%s/%s" % (tokens[2],tokens[1],tokens[0])
    else:
        return None
    
def converter_string_para_data(data_string):
    if data_string is not None and data_string != '':
        data_padrao = re.compile('\d\d/\d\d/\d\d\d\d')
        if data_padrao.match(data_string):
            data = datetime.strptime(data_string, '%d/%m/%Y')
            return data.date()
        else:
            if 'T' in data_string:
                data_string = data_string[:data_string.index('T')]
            data = datetime.strptime(data_string, '%Y-%m-%d')
            return data.date()
        
    return None

def serializar_data(data_string):
    d = converter_string_para_data(data_string)
    return formatar_data(d)

def converter_data_url(data_string):
    if data_string is not None and data_string != '':
        data = datetime.strptime(data_string, '%d%m%Y')
        return data.date()

    return None
        
    
def converter_string_para_float(float_string):
    if float_string is not None and float_string != '':
        float_string = float_string.replace('.', '').replace(',', '.')
        return float(float_string);
    else:
        return None
    
def transformar_mili_para_horas(milisegundos):
    
    if milisegundos:
        x = milisegundos / 1000 / 60
        minutos = int(x % 60)
        x /= 60
        horas = int(x)
        
        if horas < 10:
            horas = "0{0}".format(horas)
            
        if minutos < 10:
            minutos = "0{0}".format(minutos)
        
        return "%s:%s" % (horas, minutos)
        
    
