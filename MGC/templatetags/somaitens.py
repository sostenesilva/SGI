from django import template
from django.db.models import Sum
import os
import sys

caminho_absoluto = os.path.abspath('.')
sys.path.insert(0,caminho_absoluto)

from MGC import models


register = template.Library()

@register.filter
def totalPorItem(modelitem,param):
    entradaitens = models.EntradaSec.objects.filter(saldocontratosec = modelitem.saldocontratosec).values('item').annotate(SomaQTD = Sum('quantidade', default = 0))
    saidaitens = models.SaidaSec.objects.filter(saldocontratosec = modelitem.saldocontratosec).values('item').annotate(SomaQTD = Sum('quantidade', default = 0))

    if param == 'dif_total':
        for entrada in entradaitens:
            if entrada['item'] == modelitem.id:
                return modelitem.Quantidade-entrada['SomaQTD']
        return modelitem.Quantidade #CASO NENHUMA ENTRADA SEJA ENCONTRADO
        
            
    elif param == 'dif_sec':
        for entrada in entradaitens:
            if entrada['item'] == modelitem.item.id:
                for saida in saidaitens:
                    if saida['item'] == modelitem.item.id:
                        return entrada['SomaQTD']-saida['SomaQTD']
                return entrada['SomaQTD']
        return 0 #CASO NENHUMA ENTRADA OU SAÍDA SEJA ENCONTRADO
    
    elif param == 'entrada_sec':
        for entrada in entradaitens:
            if entrada['item'] == modelitem.id:
                return entrada['SomaQTD']
            
    elif param == 'saida_sec':
        for entrada in entradaitens:
            if entrada['item'] == modelitem.id:
                return saida['SomaQTD']


@register.filter
def valorTotal(item):
    return '{:.2f}'.format(item.item.PrecoUnitario * item.quantidade)