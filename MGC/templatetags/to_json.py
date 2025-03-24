import json
from django import template

register = template.Library()

@register.filter
def to_json(value):
    """Converte um objeto Python para JSON válido"""
    return json.dumps(value)
