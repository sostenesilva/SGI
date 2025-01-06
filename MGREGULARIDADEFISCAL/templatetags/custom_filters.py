from django import template

import os
import sys

caminho_absoluto = os.path.abspath('.')
sys.path.insert(0,caminho_absoluto)

register = template.Library()

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def get_choice_label(choices, value):
    """
    Mapeia o valor de um campo de escolhas para o seu rótulo humanizado.
    Exemplo:
    choices = [('FGTS', 'Certificado FGTS'), ('CNDT', 'Certidão Trabalhista')]
    value = 'FGTS'
    Retorno: 'Certificado FGTS'
    """
    return dict(choices).get(value, value)  # Retorna o rótulo ou o próprio valor se não encontrar

@register.filter
def date_format(data):
    if data.day < 10:
        day = f'0{data.day}'
    else:
        day = data.day
    
    if data.month < 10:
        month = f'0{data.month}'
    else:
        month = data.month
    
    return f'{day}/{month}/{data.year}'