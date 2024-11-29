from django.shortcuts import render
from . import models
from django.core.paginator import Paginator


def dashcombustiveis(request):
    
    context = {
    }

    return render (request,'dashcombustiveis.html',context)

def abastecimentos(request):
    abastecimentos = models.Abastecimentos.objects.all()

    buscar = request.GET.get('buscar')

    if buscar:
        abastecimentos = abastecimentos.filter(data__icontains = buscar) | abastecimentos.filter(veiculo__placa__icontains = buscar) | abastecimentos.filter(tipo__icontains = buscar) | abastecimentos.filter(condutor__username__icontains = buscar) | abastecimentos.filter(fiscal__username__icontains = buscar)
        
    abastecimentos_paginator = Paginator(abastecimentos,20)
    page_num_abastecimentos = request.GET.get('page')
    page_abastecimentos = abastecimentos_paginator.get_page(page_num_abastecimentos)
    
    context = {
        'abastecimentos': abastecimentos
    }

    return render (request,'abastecimentos/abastecimentos.html',context)
