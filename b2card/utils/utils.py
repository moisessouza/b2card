from datetime import datetime
import locale

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
        data = datetime.strptime(data_string, '%d/%m/%Y')
        return data.date()
    else:
        return None
    
def converter_string_para_float(float_string):
    float_string = float_string.replace('.', '').replace(',', '.')
    return float(float_string);
    