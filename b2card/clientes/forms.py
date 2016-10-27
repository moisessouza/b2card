from django.forms import ModelForm
from .models import Cliente

class ClienteForm(ModelForm):
    class Meta:
        model = Cliente
        fields = ['id', 'cnpj', 'razao_social', 'endereco', 'cidade', 'estado', 'cep', ]
        error_messages = {
            'NON_FIELD_ERRORS': {
                'cnpj': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }