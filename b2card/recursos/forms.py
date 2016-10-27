from django.forms import ModelForm
from .models import Funcionario

class FuncionarioForm(ModelForm):
    class Meta:
        model = Funcionario
        fields = ['id', 'nome', 'endereco', 'cidade', 'estado', 'cep', 'salario']
        error_messages = {
            'NON_FIELD_ERRORS': {
                'nome': "%(model_name)s's %(field_labels)s are not unique.",
            }
        }