from django.shortcuts import render
from datetime import date
from . import models
from MGC.models import Fornecedores

def fornecedores_list(request):
    fornecedores = Fornecedores.objects.all()
    buscar = request.GET.get('buscar')
    print(buscar)
    if buscar:
        fornecedores = Fornecedores.objects.filter(RazaoSocial__icontains=buscar)
    else:
        fornecedores = Fornecedores.objects.all()

    return render(request, 'fornecedores_list.html', {'fornecedores':fornecedores})

def certidoes_list(request, fornecedor_id):
    certidoes = models.Certidao.objects.filter(fornecedor__pk=fornecedor_id)
    return render(request, 'certidoes_list.html', {'certidoes':certidoes})

def declaracoes_list(request, fornecedor_id):
    declaracoes = models.Declaracao.objects.filter(fornecedor__pk=fornecedor_id)
    return render(request, 'declaracoes_list.html', {'declaracoes':declaracoes})

def regularidade_resumo(request, fornecedor_id):
    fornecedor = Fornecedores.objects.get(pk = fornecedor_id)
    return render(request, 'regularidade_resumo.html', {'fornecedor':fornecedor})

def emitir_declaracao(fornecedor):
    fornecedor = fornecedor
    declaracao = models.Declaracao.objects.create(fornecedor=fornecedor)
    certidoes = declaracao.get_certidoes()

    # Verifica se todas as certidões foram encontradas
    faltando = [tipo for tipo, certidao in certidoes.items() if certidao is None]
    if faltando:
        print(f"Certidões faltando: {', '.join(faltando)}")

    return declaracao, certidoes

def dashregularidade(request):
    # fornecedor = Fornecedores.objects.get(pk = 1)
    # print(fornecedor)

    # declaracao, certidoes = emitir_declaracao(fornecedor)
    # print(declaracao)
    # print(certidoes)
    return render(request,'dashregularidadefiscal.html', {})
