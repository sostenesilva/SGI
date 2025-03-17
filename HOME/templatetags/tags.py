from django import template
from django.contrib.auth.models import Group, Permission, User
import os
import sys
from django.shortcuts import get_object_or_404

caminho_absoluto = os.path.abspath('.')
sys.path.insert(0,caminho_absoluto)

register = template.Library()

@register.filter
def has_perm_modulo(user, modulo):
    codename = f'autorizado_Acessar_{modulo.sigla}'
    # print(f'Codename: {codename}')
    perm = get_object_or_404(Permission, codename=codename)
    # print(f'Permissão: {perm}')
    permissoes_usuario = list(user.user_permissions.values_list("id", flat=True))
    # print(f'Autorizado: {perm.id in permissoes_usuario}')
    if user.is_superuser:
        return True
    
    return perm.id in permissoes_usuario