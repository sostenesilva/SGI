import base64
from functools import reduce
from operator import or_, itemgetter
from django.http import JsonResponse
from django.shortcuts import render,redirect, HttpResponse
from weasyprint import HTML
from . import forms, models
from django.contrib.auth.models import Group, User
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import date, datetime
import requests, json
from docx import Document, document, table
from python_docx_replace import docx_replace
import pandas as pd
import uuid
from django.db.models import Sum
from django.contrib import messages
from django.template.loader import render_to_string



#------------------- PÁGINAS DE DASHBOARD -------------------#
@login_required
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
@login_required
def contratos (request):

    
    buscar = request.GET.get('buscar')
    if buscar:
        contratos = models.Contratos.objects.filter(Fornecedor__RazaoSocial__icontains = buscar) | models.Contratos.objects.filter(NumeroContrato__icontains = buscar) | models.Contratos.objects.filter(NumeroProcesso__icontains = buscar) | models.Contratos.objects.filter(AnoContrato__icontains = buscar) | models.Contratos.objects.filter(AnoProcesso__icontains = buscar)
    else:
        contratos = models.Contratos.objects.all()
        
    contratos_paginator = Paginator(contratos,20)
    page_num_contratos = request.GET.get('page')
    page_contratos = contratos_paginator.get_page(page_num_contratos)
    
    context = {
        'contratos': page_contratos
    }
    
    return render(request, 'listar_contratos.html', context)

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

@login_required
def contratos_addsaldosec(request,contrato_pk):
    contrato = models.Contratos.objects.get(pk=contrato_pk) #INSTÂNCIA DO CONTRATO ATUAL
    
    #FORMULÁRIOS
    saldocontratosec_form = forms.SaldoContratoSec_form(request.POST or None)
    
    itenscontrato = models.Itens.objects.filter(Contrato=contrato) #FILTRAR ITENS DO CONTRATO

    if request.POST:
        quantidades = request.POST.getlist('quantidade')
        item_ids = request.POST.getlist('item_id')
        saldocontratosec = saldocontratosec_form.save(commit=False)
        saldocontratosec.contrato = contrato
        saldocontratosec.save()
        
        for item_id,qtd in zip(item_ids,quantidades):
            if qtd and int(qtd) > 0:
                entradasec = models.EntradaSec.objects.create(
                    saldocontratosec = saldocontratosec,
                    item = models.Itens.objects.get(pk = item_id),
                    quantidade = int(qtd),
                    usuario = request.user
                )
                entradasec.save()
        return redirect('contratos')
    
    context = {
        'saldocontratosec_form': saldocontratosec_form,
        'contrato': contrato,
        'itenscontrato': itenscontrato,
    }

    return render(request, 'add_saldosec.html',context)


@login_required
def contratos_additens(request,contrato_pk):
    contrato = models.Contratos.objects.get(pk=contrato_pk)
    itensof = models.Itens.objects.all()
    
    if request.POST:
        dataframe = pd.read_excel(request.FILES.get('itens'))
        for index, row in dataframe.iterrows():
            itemadd, itembool = models.Itens.objects.update_or_create(
                Descricao = row[0],
                Unidade = row[1],
                Contrato = contrato,
                PrecoUnitario = float(str(row[3])),
                Quantidade = str(str(row[2])),
                Quantidade_disp = str(str(row[2])),
                # PrecoTotal = float(str(row[4])),
            )
            
            itemadd.save()
        contrato.AtualizarItens = False
        contrato.save()

        return redirect('contratos')
    
    context = {
    }

    return render(request, 'contratos/contratos_additens.html',context)

def contratos_request2(request):
    return render(request, 'contratos_request.html')


#PÁGINA ADD_CONTRATOS
@login_required
def add_contratos(request):
    return render(request, 'add_contratos.html')

#CONTRATOS LICON
@login_required
def contratos_request(request):
    ano = request.GET.get('ano', '2025')  # Padrão para 2025 se não for informado
     # Buscar contratos e processos na API do TCE-PE
    contratos_licon = requests.get(
        f'https://sistemas.tcepe.tc.br/DadosAbertos/Contratos!json?UnidadeOrcamentaria=Prefeitura&Esfera=M&Municipio=Cortes&AnoContrato={ano}'
    ).json()['resposta']['conteudo']

    processos_licon = requests.get(
        f'https://sistemas.tcepe.tc.br/DadosAbertos/LicitacoesDetalhes!json?CODIGOUG=211&UG=CORTES&ANOMODALIDADE={ano}&CODIGOMUNICIPIO=P050'
    ).json()['resposta']['conteudo']

    # Criar um dicionário associando os códigos PL aos objetos dos processos
    processos_dict = {proc['CODIGOPL']: proc for proc in processos_licon}

    # Adicionar detalhes do processo ao contrato
    for contrato in contratos_licon:
        codigo_pl = contrato.get('CodigoPL')
        if codigo_pl and codigo_pl in processos_dict:
            contrato['Objeto'] = processos_dict[codigo_pl].get('OBJETOCONFORMEEDITAL', '')
            contrato['LinkEdital'] = processos_dict[codigo_pl].get('LinkArquivo', '')
    # 🔹 Passo 2: Buscar contratos já cadastrados no banco de dados
    contratos_existentes = models.Contratos.objects.all()

    # 🔹 Lista para armazenar contratos com grau de similaridade
    contratos_comparados = []

    for contrato in contratos_licon:
        # Pegar os dados do contrato da API
        numero_contrato_api = contrato.get('NumeroContrato')
        ano_contrato_api = contrato.get('AnoContrato')
        fornecedor_api = contrato.get('RazaoSocial')
        objeto_api = contrato.get('Objeto', '').strip()
        valor_api = float(contrato.get('Valor', 0))
        
        # Inicializar grau de similaridade
        grau_similaridade = 0

        # Verificar se existe um contrato semelhante no banco
        contrato_existente = contratos_existentes.filter(NumeroContrato=numero_contrato_api, AnoContrato=ano_contrato_api).all()

        if contrato_existente:
            for contrato_x in contrato_existente:
                # Comparação de cada critério e soma de pontos
                if contrato_x.Fornecedor.RazaoSocial == fornecedor_api:
                    # print(f'{contrato_existente.Fornecedor.RazaoSocial} == {fornecedor_api}')
                    grau_similaridade += 25  # Fornecedor igual → 25%

                if contrato_x.Objeto and contrato_x.Objeto.strip().lower() == objeto_api.lower():
                    # print(f'{contrato_existente.Objeto and contrato_existente.Objeto.strip().lower()} == {objeto_api.lower()}')
                    grau_similaridade += 25  # Objeto igual → 25%

                if contrato_x.Valor == valor_api:
                    # print(f'{contrato_existente.Valor} == {valor_api}')

                    grau_similaridade += 25  # Valor igual → 25%

                if contrato_x.NumeroContrato == numero_contrato_api:
                    # print(f'{contrato_existente.NumeroContrato} == {numero_contrato_api}')

                    grau_similaridade += 25  # Número do contrato igual → 25%

        # Definir um nível de similaridade baseado na pontuação
        if grau_similaridade >= 100:
            grau_similaridade = 100
            badge = "bg-success text-white"  # Muito semelhante (100%)
        elif grau_similaridade >= 50:
            badge = "bg-warning text-dark"  # Parcialmente semelhante (50-75%)
        else:
            badge = "bg-danger text-white"  # Pouco semelhante (0-25%)

        # Adicionar contrato à lista com grau de similaridade
        contratos_comparados.append({
            'contrato': contrato,
            'grau_similaridade': grau_similaridade,
            'badge': badge,
        })
        contratos_comparados = sorted(contratos_comparados, key=lambda x: x['grau_similaridade'])
        # contratos_comparados = sorted(contratos_comparados, key=contratos_comparados[1], reverse=True)

    # Renderizar a página com os contratos para seleção
    return render(request, 'contratos_request.html', {'contratos': contratos_comparados})



def processar_contratos_selecionados(request):
    if request.method == "POST":
        contratos_json = request.POST.getlist("selecionados")  # Pegando os contratos selecionados

        if not contratos_json:
            messages.error(request, "Nenhum contrato selecionado.")
            return redirect("contratos")  # Redireciona para a lista

        contratos_lista = []
        try:
            for contratos in contratos_json:
                json_acceptable_string = contratos.replace("'", "\"")
                contratos_lista.append(json.loads(json_acceptable_string))  # Converte a string JSON para lista de dicionários
            
        except json.JSONDecodeError:
            print('json decode error')
            messages.error(request, "Erro ao processar os contratos selecionados.")
            return redirect("contratos")

        contratos_cadastrados = []

        for contrato_data in contratos_lista:
            # Primeiro, garantir que o fornecedor existe
            fornecedor, created = models.Fornecedores.objects.get_or_create(
                RazaoSocial=contrato_data["RazaoSocial"],
                CPF_CNPJ=contrato_data["CPF_CNPJ"]
            )
            fornecedor.NumeroDocumentoAjustado = contrato_data["NumeroDocumento"]
            fornecedor.save()

            # Criar ou atualizar contrato
            contrato = models.Contratos.objects.create(
                NumeroContrato=contrato_data["NumeroContrato"],
                AnoContrato=contrato_data["AnoContrato"],
                Fornecedor = fornecedor,
                TipoProcesso = contrato_data.get("TipoProcesso", ""),
                NumeroProcesso = contrato_data.get("NumeroProcesso", ""),
                AnoProcesso = contrato_data.get("AnoProcesso", ""),
                Valor = float(contrato_data.get("Valor", 0)),
                LinkContrato = contrato_data.get("LinkArquivo", ""),
                Objeto = contrato_data.get("Objeto", ""),
                LinkEdital = contrato_data.get("LinkEdital", ""),
            )

            vigencia = contrato_data.get("Vigencia","").split(" a ")
            contrato.data_inicio = datetime.strptime(vigencia[0], "%d/%m/%Y").date()
            contrato.data_fim = datetime.strptime(vigencia[1], "%d/%m/%Y").date()
            contrato.save()

            contratos_cadastrados.append(f"{contrato.NumeroContrato}/{contrato.AnoContrato}")

        if contratos_cadastrados:
            messages.success(request, f"Contratos cadastrados: {', '.join(contratos_cadastrados)}")
        else:
            messages.info(request, "Nenhum novo contrato foi cadastrado.")

        return redirect("contratos")  # Altere para a URL correta
    else:
        return redirect("contratos")




#------------------- PÁGINAS DE ORDEM DE FORNECIMENTO -------------------#
@login_required
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

@login_required
def painelfiscal (request):

    SaldoContratoSec = models.SaldoContratoSec.objects.filter(fiscal= request.user)
    ordens_paginator = Paginator(SaldoContratoSec,30)
    page_num_ordens = request.GET.get('page')
    page_ordens = ordens_paginator.get_page(page_num_ordens)
 
    context = {
        'ordens': page_ordens,
        'contrato': contratos,
    }
    
    return render(request, 'ordens/painelfiscal.html', context)

def saldo_detalhes (request,saldodetalhes_pk):
    SaldoContratoSec = models.SaldoContratoSec.objects.get(pk=saldodetalhes_pk)
    ContratoSec = SaldoContratoSec.contrato


    itensof = models.Itens.objects.filter(Contrato=ContratoSec)
    entradasSec = models.EntradaSec.objects.filter(saldocontratosec=SaldoContratoSec)


    Ordem_hist = models.Ordem.objects.filter(saldoContratosec=SaldoContratoSec).order_by('-dataehora')
    
    ordens_paginator = Paginator(Ordem_hist,6)
    page_num_ordens = request.GET.get('page')
    page_ordens_log = ordens_paginator.get_page(page_num_ordens)

    consumido = 0
    # for ordem in Ordem_hist:
    #     consumido += ordem.valor


    context = {
        'page_ordens_log': page_ordens_log,
        'contrato': ContratoSec,
        'SaldoContratoSec': SaldoContratoSec,
        'consumido': consumido,
        'itensof': itensof,
        'itemEntrada': entradasSec,
    }

    return render(request, 'ordens/ordens_detalhes.html',context)

def of_emitir (request,saldodetalhes_pk):
    SaldoContratoSec = models.SaldoContratoSec.objects.get(pk=saldodetalhes_pk)
    ContratoSec = SaldoContratoSec.contrato

    itensof = models.Itens.objects.filter(Contrato=ContratoSec)
    entradasSec = models.EntradaSec.objects.filter(saldocontratosec=SaldoContratoSec)

    ordem_form = forms.Ordem_form(request.POST or None)

    if request.POST:
        item_ids = request.POST.getlist('item_id')
        quantidades = request.POST.getlist('quantidade')

        ordem = models.Ordem.objects.create(saldoContratosec = SaldoContratoSec,usuario = request.user, valor = 0)
        valordaordem = 0
        listaitens = []
        for item_id,qtd in zip(item_ids,quantidades):
            # print(f'Item: {item_id} - {qtd}')
            if qtd and int(qtd) > 0:
                saidasec = models.SaidaSec()

                saidasec.ordem = ordem
                saidasec.item = itensof.get(pk = item_id)
                saidasec.quantidade = int(qtd)
                saidasec.usuario = request.user

                valordaordem += (saidasec.item.PrecoUnitario * saidasec.quantidade)
                # print(f'Preço unitário: {saidasec.item.PrecoUnitario} - Quantidade: {saidasec.quantidade} - Total: {saidasec.item.PrecoUnitario * saidasec.quantidade} - Acumulado: {valordaordem} - Tipo: {type(valordaordem)}')
                listaitens.append(saidasec)
                saidasec.save()

        ordem.descricao = request.POST.get('descricao')
        ordem.valor = valordaordem
        ordem.codigo = uuid.uuid4()
        ordem.arquivo = emitirDocOf(request, ordem ,listaitens)
        ordem.save()
        return redirect('saldo_detalhes', SaldoContratoSec.id)

    context = {
        'ordem_form': ordem_form,
        'contrato': ContratoSec,
        'SaldoContratoSec': SaldoContratoSec,
        'entradasSec': entradasSec,
    }

    return render(request, 'ordens_emitir.html',context)

def emitirOF (request, ordem, listadeitens):
    with open("static/img/bg-timbrado-logo.png", "rb") as image_file:
        page_background = base64.b64encode(image_file.read()).decode('utf-8')

    # Gerar HTML com contexto atualizado
    html_string = render_to_string('ordem_pdf.html', {
        'page_background': page_background,
        'ordem': ordem,
        'listadeitens':listadeitens
    })

    # Caminho absoluto do CSS
    base_url = request.build_absolute_uri('/')

    # Gerar PDF
    pdf_file = HTML(string=html_string, base_url=base_url).write_pdf()

    # Retornar o PDF para download
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ordem_1.pdf"'
    return response

def emitirDocOf (request, ordem, listadeitens):
    document = Document("media/ordem de fornecimento/MODELO ORDEM DE FORNECIMENTO.docx")
    
    tabela = document.tables[0]
    nItem = 1
    for itemlista in listadeitens:
        row = tabela.add_row().cells
        row[0].text = str(nItem)
        row[1].text = itemlista.item.Descricao
        row[2].text = str(itemlista.quantidade)
        row[3].text = itemlista.item.Unidade
        row[4].text = 'R$ '+ f'{itemlista.item.PrecoUnitario:.2f}'.replace('.',',')
        totalporitem = itemlista.quantidade*itemlista.item.PrecoUnitario
        row[5].text = 'R$ '+ f'{totalporitem:.2f}'.replace('.',',')
        nItem += 1
    mes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
    mydict = {
        'idOrdem': f'{ordem.codigo}',
        'descricaoDaOF': ordem.descricao,
        'valorTotalOF': f'{ordem.valor:.2f}'.replace('.',','),
        'contratada': ordem.saldoContratosec.contrato.Fornecedor.RazaoSocial,
        'cnpj': ordem.saldoContratosec.contrato.Fornecedor.NumeroDocumentoAjustado,
        'data': f'{ordem.dataehora.day} de {mes[ordem.dataehora.month-1]} de {ordem.dataehora.year}',
        'contrato': f'{ordem.saldoContratosec.contrato.NumeroContrato}/{ordem.saldoContratosec.contrato.AnoContrato}',
        'processo': f'{ordem.saldoContratosec.contrato.NumeroProcesso}/{ordem.saldoContratosec.contrato.AnoProcesso}',
        'ug': f'{ordem.saldoContratosec.contrato.UnidadeOrcamentaria.upper()}',
        'endereco': f'{ordem.saldoContratosec.contrato.Fornecedor.Endereco}',
        'representante': f'{ordem.saldoContratosec.contrato.Fornecedor.Representante}',
        'fone': f'{ordem.saldoContratosec.contrato.Fornecedor.Contato}',
        'email': f'{ordem.saldoContratosec.contrato.Fornecedor.Email}',
        'objeto': f'{ordem.saldoContratosec.contrato.Objeto}',
    }

    docx_replace(document, **mydict )
    diretorio = f'media/ordem de fornecimento/2025/{ordem}.docx'
    document.save(diretorio)

    return diretorio

# def emitirDocPagamento (request, ordem, listadeitens):
#     document = Document("media/solicitação de pagamento/SOLICITAÇÃO DE PAGAMENTO - MODELO.docx")

#     # for itemlista in listadeitens:
#     #     row = tabela.add_row().cells
#     #     row[0].text = str(nItem)
#     #     row[1].text = itemlista.item.Descricao
#     #     row[2].text = str(itemlista.quantidade)
#     #     row[3].text = itemlista.item.Unidade
#     #     row[4].text = 'R$ '+ f'{itemlista.item.PrecoUnitario:.2f}'.replace('.',',')
#     #     row[5].text = 'R$ '+ f'{itemlista.totalporitem:.2f}'.replace('.',',')
#     #     nItem += 1
#     mes = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro']
#     mydict = {
#         'idOrdem': ordem.id,
#         'descricaoDaOF': ordem.descricao,
#         'valorTotalOF': f'{ordem.valor:.2f}'.replace('.',','),
#         'contratada': ordem.SaldoContratoSec.contrato.Fornecedor.RazaoSocial,
#         'cnpj': ordem.SaldoContratoSec.contrato.Fornecedor.NumeroDocumentoAjustado,
#         'data': f'{ordem.dataehora.day} de {mes[ordem.dataehora.month-1]} de {ordem.dataehora.year}',
#         'contrato': f'{ordem.SaldoContratoSec.contrato.NumeroContrato}/{ordem.SaldoContratoSec.contrato.AnoContrato}',
#         'processo': f'{ordem.SaldoContratoSec.contrato.NumeroProcesso}/{ordem.SaldoContratoSec.contrato.AnoProcesso}',
#         'ug': f'{ordem.SaldoContratoSec.contrato.UnidadeOrcamentaria.upper()}',
#         'endereco': f'{ordem.SaldoContratoSec.contrato.Fornecedor.Endereco}',
#         'representante': f'{ordem.SaldoContratoSec.contrato.Fornecedor.Representante}',
#         'fone': f'{ordem.SaldoContratoSec.contrato.Fornecedor.Contato}',
#         'email': f'{ordem.SaldoContratoSec.contrato.Fornecedor.Email}',
#         'objeto': f'{ordem.SaldoContratoSec.contrato.Objeto}',
#     }

#     docx_replace(document, **mydict )
#     diretorio = f'media/ordem de fornecimento/2024/{ordem.id}.docx'
#     document.save(diretorio)
#     return diretorio

def of_edit (request, saldoof_pk):
    pass
 
@login_required
def of_log_delet(request, saldoof_pk, of_log_pk):
    of_log = models.Ordem.objects.get(pk=of_log_pk)
    of_log.delete()
    return redirect (request.META.get('HTTP_REFERER'))









# #------------------- PÁGINAS DE AVALIAÇÃO -------------------#
# @login_required
# def avaliacao (request):

#     if has_role(request.user, Controle):
#         avaliacao = models.Db_Avaliacao.objects.all()
#     else:
#         avaliacao = models.Db_Avaliacao.objects.filter(responsavel__in = request.user.groups.all())

#     avaliacao_paginator = Paginator(avaliacao,10)
#     page_num_avaliacao = request.GET.get('page')
#     page_avaliacao = avaliacao_paginator.get_page(page_num_avaliacao)

#     context = {
#         'avaliacao': page_avaliacao
#     }
    
#     return render(request, 'avaliacao/avaliacao.html', context)

# #AVALIAÇÃO ADD
# @login_required
# def avaliacao_add (request):
#     avaliacao_form = forms.Avaliacao_form(request.POST or None)

#     if request.POST:
#         if avaliacao_form.is_valid():
#             avaliacao_form.save()
#             return redirect ('avaliacao')

#     context = {
#         'avaliacao_form': avaliacao_form
#     }
#     return render(request, 'avaliacao/avaliacao_add.html',context)

# #AVALIAÇÃO EDIT
# @login_required
# def avaliacao_edit(request, avaliacao_pk):
#     avaliacao = models.Db_Avaliacao.objects.get(pk=avaliacao_pk)

#     avaliacao_form = forms.Avaliacao_form(request.POST or None, instance = avaliacao)

#     if request.POST:
#         if avaliacao_form.is_valid():
#             avaliacao.arquivo = request.FILES.get('arquivo')
#             avaliacao_form.save()
#             return redirect ('avaliacao')
    
#     context = {
#         'avaliacao_form': avaliacao_form
#     }

#     return render(request, 'avaliacao/avaliacao_edit.html',context)

# #AVALIAÇÃO DELET
# @login_required
# def avaliacao_delet(request, avaliacao_pk):
#     avaliacao = models.Db_Avaliacao.objects.get(pk=avaliacao_pk)
#     avaliacao.delete()
#     return redirect('avaliacao')


#AVALIAÇÃO DELETE
@login_required
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
