from django.shortcuts import render,redirect, HttpResponse
from . import forms, models
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import date
import requests, json

#------------------- PÁGINAS DE DASHBOARD -------------------#
def dashboard(request):
    
    context = {
    }

    return render (request,'dashboard/dashboard.html',context)

#  
# def configuracoes(request):
    
#     usuarios = User.objects.all()

#     if request.POST:
#         user = usuarios.get(username = request.POST.get('usuario'))
#         funcao = request.POST.get('funcaocheck')
#         if funcao == 'gestor':
#             assign_role(user,'fmas')
#             grant_permission(user, 'gestor')
#             #grant_permission(user, 'fiscal')
#         if funcao == 'fiscal':
#             assign_role(user,'fmas')

#             #grant_permission(user, 'fiscal')
#            # revoke_permission(user, 'gestor')


#     context = {
#         'usuarios': usuarios,
#     }

#     return render (request,'dashboard/configuracoes.html',context)

#------------------- PÁGINAS DE CONTRATOS -------------------#
def contratos (request):

    contratos = models.Contratos.objects.all()

    contratos_paginator = Paginator(contratos,20)
    page_num_contratos = request.GET.get('page')
    page_contratos = contratos_paginator.get_page(page_num_contratos)
 
    context = {
        'contratos': page_contratos
    }
    
    return render(request, 'contratos/contratos.html', context)

#CONTRATO ADD
#   
# def contratos_add (request, processo_pk):
#     processo = models.Processos.objects.get(pk=processo_pk)
#     contratos_form = forms.Contratos_form(request.POST or None)
#     contratos_form.instance.processo = processo

#     if request.POST:
#         if contratos_form.is_valid():
#             contratos_form.save()
#             return redirect ('contratos')

#     context = {
#         'contratos_form': contratos_form,
#         'processo': processo
#     }
#     return render(request, 'contratos/contratos_add.html',context)

#CONTRATO EDIT
#   
# def contrato_edit(request, contrato_pk):
#     contrato = models.Contratos.objects.get(pk=contrato_pk)

#     contrato_form = forms.Contratos_form(request.POST or None, instance = contrato)

#     if request.POST:
#         if contrato_form.is_valid():
#             contrato_form.save()
#             return redirect ('contratos')
    
#     context = {
#         'contratos_form': contrato_form
#     }

#     return render(request, 'contratos/contratos_edit.html',context)

#CONTRATO DELET
#   
# def contrato_delet(request, contrato_pk):
#     contrato = models.Contratos.objects.get(pk=contrato_pk)
#     contrato.delete()
#     return redirect('contratos')

#CONTRATO ENVIAR   - READAPTAR BACKEND PARA OS BANCOS DE OF
#  
# def contrato_enviar(request, contrato_pk):
#     contrato = models.Contratos.objects.get(pk=contrato_pk)
#     contrato_saldoof = models.SaldoSec(contrato=contrato)
#     contrato_saldoof_hist = models.Ordem.objects.filter(saldoof=contrato_saldoof).order_by('-dataehora')
    
#     contrato_form = forms.Contratos_form(request.POST or None)
    
#     if request.POST:
#         if contrato_form.is_valid() and (request.FILES.get('arquivo')):
#             # contrato_of.arquivo = request.FILES.get('arquivo')
#             # contrato_of.usuario = request.user

#             # contrato_of.save()
            
#             return redirect (request.path_info)

#     contrato_saldoof_paginator = Paginator(contrato_saldoof_hist,6)
#     page_num_contrato_saldoof = request.GET.get('page')
#     page_avaliacao_log = contrato_saldoof_paginator.get_page(page_num_contrato_saldoof)


#     context = {
#         'avaliacao_log_hist': page_avaliacao_log,
#         'contrato': contrato,
#         'processo': contrato.processo
#     }

#     return render(request, 'contratos/contratos_enviarof.html',context)

def contratos_add_of(request,contrato_pk):
    contrato = models.Contratos.objects.get(pk=contrato_pk)
    of_form = forms.SaldoSec_form(request.POST or None)
    itensof = models.Itens.objects.filter(CodigoContratoOriginal=contrato.CodigoContrato)
    controleEntradas = models.EntradaSec.objects.filter(contrato=contrato)
    
    if request.POST:
        cestaitens = enumerate(request.POST.getlist('quantidade'))
        SaldoContratoSec, ContratoSecCriado = models.SaldoContratoSec.objects.update_or_create(contrato = contrato, sec = models.Group.objects.get(pk=request.POST['sec']))
        for itemcesta,qtd in cestaitens:
            if qtd != '0':
                entradasec = models.EntradaSec()
                entradasec.contrato = contrato
                entradasec.item = itensof[itemcesta]
                entradasec.quantidade = int(qtd)
                SaldoContratoSec.saldo += (entradasec.item.PrecoUnitario * entradasec.quantidade)
                entradasec.sec = models.Group.objects.get(pk=request.POST['sec'])
                entradasec.usuario = request.user
                entradasec.save()

        
        SaldoContratoSec.save()
        return redirect('contratos')
    
    context = {
        'of_form': of_form,
        'contrato': contrato,
        'itensof': itensof,
    }

    return render(request, 'ordens/ordens_add.html',context)

#CONTRATOS LICON
def contratos_request(request):
    contratos_licon = requests.get('https://sistemas.tcepe.tc.br/DadosAbertos/Contratos!json?UnidadeOrcamentaria=Prefeitura&Esfera=M&Municipio=Cortes&AnoContrato=2024').json()['resposta']['conteudo']
    processos_licon = requests.get('https://sistemas.tcepe.tc.br/DadosAbertos/LicitacaoUG!json?UG=CORTES').json()['resposta']['conteudo']
    
    for contrato in contratos_licon:
        #print('Contrato {}/{} - UG: {} - Tipo: {}'.format(contrato['NumeroContrato'],contrato['AnoContrato'],contrato['UnidadeGestora'],contrato['TipoProcesso']))
        try:
            cont, cont_criado = models.Contratos.objects.update_or_create(
                NumeroContrato = contrato['NumeroContrato'],
                AnoContrato = contrato['AnoContrato'],
                TipoProcesso = contrato['TipoProcesso'], 
                NumeroProcesso = contrato['NumeroProcesso'], 
                AnoProcesso = contrato['AnoProcesso'], 
                UnidadeGestora = contrato['UnidadeGestora']
                )
        except:
            cont, cont_criado = models.Contratos.objects.update_or_create(
                NumeroContrato = contrato['NumeroContrato'],
                AnoContrato = contrato['AnoContrato'], 
                UnidadeGestora = contrato['UnidadeGestora'],
                RazaoSocial = contrato['RazaoSocial']
                )
        
        cont.NumeroDocumentoAjustado = contrato['NumeroDocumentoAjustado'].replace(' ','')
        cont.RazaoSocial = contrato['RazaoSocial']
        cont.CPF_CNPJ = contrato['CPF_CNPJ']
        cont.LinkContrato = contrato['LinkArquivo']
        cont.Situacao = contrato['Situacao']
        cont.SiglaUG = contrato['SiglaUG']
        cont.Valor = float(contrato['Valor'])
        cont.UnidadeOrcamentaria = contrato['UnidadeOrcamentaria']
        cont.CodigoUG = contrato['CodigoUG']
        #cont.PortariaComissaoLicitacao = contrato['PortariaComissaoLicitacao']
        cont.CodigoContrato = contrato['CodigoContrato']
        cont.Vigencia = contrato['Vigencia']
        cont.Estagio = contrato['Estagio']
        #cont.CodigoPL = contrato['CodigoPL']
        cont.NumeroDocumento = contrato['NumeroDocumento']
        cont.Municipio = contrato['Municipio']
        cont.TipoDocumento = contrato['TipoDocumento']
        cont.Esfera = contrato['Esfera']

        for processo in processos_licon:
            if cont.CodigoPL == processo['CODIGOPL']:    
                cont.Objeto = processo['OBJETOCONFORMEEDITAL']
                cont.LinkEdital = processo['LinkArquivo']
    
        cont.save()


        itens_licon = requests.get('https://sistemas.tcepe.tc.br/DadosAbertos/ContratoItemObjeto!json?CodigoContratoOriginal={}'.format(cont.CodigoContrato)).json()['resposta']['conteudo']
        for item in itens_licon:
            print(item)
            print()
            itemcontrato, itemcontrato_criado = models.Itens.objects.update_or_create(
                CodigoContratoOriginal = item['CodigoContratoOriginal'],
                CodigoItem = item['CodigoItem']
            )
            itemcontrato.Descricao = item['Descricao']
            itemcontrato.Unidade = item['Unidade']
            itemcontrato.PrecoUnitario = float(item['PrecoUnitario'])
            itemcontrato.Quantidade = float(item['Quantidade'])
            itemcontrato.PrecoTotal = float(item['PrecoTotal'])
            itemcontrato.save()

    return redirect('contratos')


#------------------- PÁGINAS DE ORDEM DE FORNECIMENTO -------------------#
def ordens (request):
    
    SaldoContratoSec = models.SaldoContratoSec.objects.all()
    # if has_role(request.user,'controle'):
    #    SaldoContratoSec = models.SaldoContratoSec.objects.all()
    # else: 
    #     SaldoContratoSec = models.SaldoContratoSec.objects.filter(sec=request.user.groups.all()[0])

    ordens_paginator = Paginator(SaldoContratoSec,30)
    page_num_ordens = request.GET.get('page')
    page_ordens = ordens_paginator.get_page(page_num_ordens)
 
    context = {
        'ordens': page_ordens,
        'contrato': contratos,
    }
    
    return render(request, 'ordens/ordens.html', context)

def of_enviar (request,saldoof_pk):
    SaldoContratoSec = models.SaldoContratoSec.objects.get(pk=saldoof_pk)
    ContratoSec = SaldoContratoSec.contrato
    itensof = models.Itens.objects.filter(CodigoContratoOriginal=ContratoSec.CodigoContrato)
    Ordem_hist = models.Ordem.objects.filter(SaldoContratoSec=SaldoContratoSec).order_by('-dataehora')
        
    ordens_paginator = Paginator(Ordem_hist,6)
    page_num_ordens = request.GET.get('page')
    page_ordens_log = ordens_paginator.get_page(page_num_ordens)

    consumido = 0
    for ordem in Ordem_hist:
        consumido += ordem.valor

    saldodisponivel = SaldoContratoSec.saldo - consumido

    context = {
        'page_ordens_log': page_ordens_log,
        'contrato': ContratoSec,
        'SaldoContratoSec': SaldoContratoSec,
        'consumido': consumido,
        'saldodisponivel': saldodisponivel,
        'itensof': itensof,
    }

    return render(request, 'ordens/ordens_detalhes.html',context)

def of_emitir (request,saldoof_pk):
    SaldoContratoSec = models.SaldoContratoSec.objects.get(pk=saldoof_pk)
    ContratoSec = SaldoContratoSec.contrato
    itensof = models.Itens.objects.filter(CodigoContratoOriginal=ContratoSec.CodigoContrato)

    ContratoSec_hist = models.Ordem.objects.filter(SaldoContratoSec = SaldoContratoSec).order_by('-dataehora')

    ordem_form = forms.Ordem_form(request.POST or None)

    if request.POST:
        print(request.POST)
        cestaitens = enumerate(request.POST.getlist('quantidade'))
        ordem = models.Ordem.objects.create(SaldoContratoSec = SaldoContratoSec, usuario = request.user)
        valordaordem = 0
        
        for itemcesta,qtd in cestaitens:
            print('estou aqui 1')
            if qtd != '0':
                print('estou aqui 2')

                saidasec = models.SaidaSec()
                saidasec.contrato = ContratoSec
                saidasec.ordem = ordem
                saidasec.item = itensof[itemcesta]
                saidasec.quantidade = int(qtd)
                saidasec.usuario = request.user

                valordaordem += (saidasec.item.PrecoUnitario * saidasec.quantidade)

                saidasec.save()


        ordem.descricao = request.POST.get('descricao')
        ordem.valor = valordaordem
        ordem.save()
        return redirect('ordens')

    context = {
        'ordem_form': ordem_form,
        'contrato': ContratoSec,
        'SaldoContratoSec': SaldoContratoSec,
        'itensof': itensof,
    }

    return render(request, 'ordens/ordens_emitir.html',context)

def of_edit (request, saldoof_pk):
    pass

 
def of_delet (request, saldoof_pk):
    pass



#------------------- PÁGINAS DE AVALIAÇÃO -------------------#
 
def avaliacao (request):

    if has_role(request.user, Controle):
        avaliacao = models.Db_Avaliacao.objects.all()
    else:
        avaliacao = models.Db_Avaliacao.objects.filter(responsavel__in = request.user.groups.all())

    avaliacao_paginator = Paginator(avaliacao,10)
    page_num_avaliacao = request.GET.get('page')
    page_avaliacao = avaliacao_paginator.get_page(page_num_avaliacao)

    context = {
        'avaliacao': page_avaliacao
    }
    
    return render(request, 'avaliacao/avaliacao.html', context)

#AVALIAÇÃO ADD
def avaliacao_add (request):
    avaliacao_form = forms.Avaliacao_form(request.POST or None)

    if request.POST:
        if avaliacao_form.is_valid():
            avaliacao_form.save()
            return redirect ('avaliacao')

    context = {
        'avaliacao_form': avaliacao_form
    }
    return render(request, 'avaliacao/avaliacao_add.html',context)

#AVALIAÇÃO EDIT
def avaliacao_edit(request, avaliacao_pk):
    avaliacao = models.Db_Avaliacao.objects.get(pk=avaliacao_pk)

    avaliacao_form = forms.Avaliacao_form(request.POST or None, instance = avaliacao)

    if request.POST:
        if avaliacao_form.is_valid():
            avaliacao.arquivo = request.FILES.get('arquivo')
            avaliacao_form.save()
            return redirect ('avaliacao')
    
    context = {
        'avaliacao_form': avaliacao_form
    }

    return render(request, 'avaliacao/avaliacao_edit.html',context)

#AVALIAÇÃO DELET
def avaliacao_delet(request, avaliacao_pk):
    avaliacao = models.Db_Avaliacao.objects.get(pk=avaliacao_pk)
    avaliacao.delete()
    return redirect('avaliacao')


#AVALIAÇÃO DELETE
def avaliacao_log_delet(request, avaliacao_pk, avaliacao_log_pk):
    avaliacao_log = models.Db_Avaliacao_log.objects.get(pk=avaliacao_log_pk)
    avaliacao_log.delete()
    return redirect (request.META.get('HTTP_REFERER'))


# def controle(request):
#     assign_role(request.user, 'controle')
#     return HttpResponse('CONTROLE INTERNO ADICIONADO!')

# def secadm(request):
#     assign_role(request.user, 'sec_adm')
#     return HttpResponse('SECRETARIA DE ADMINISTRAÇÃO ADICIONADA!')