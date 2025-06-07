import json
import os
import uuid
from django.http import HttpResponse
from django.shortcuts import redirect, render
from datetime import date, datetime
from weasyprint import CSS, HTML
from docx import Document
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from python_docx_replace import docx_replace
import base64
from SGI import settings
from . import models, forms
from django.forms import formset_factory, modelformset_factory
from MGC.models import Fornecedores
from django.template.loader import render_to_string
from django.core.files.base import ContentFile

def fornecedores_list(request):
    fornecedores = Fornecedores.objects.all()
    buscar = request.GET.get('buscar')
    if buscar:
        fornecedores = Fornecedores.objects.filter(RazaoSocial__icontains=buscar)
    else:
        fornecedores = Fornecedores.objects.all()
    return render(request, 'fornecedores_list.html', {'fornecedores':fornecedores})

def certidoes_list(request, fornecedor_id):
    certidoes = models.Certidao.objects.filter(fornecedor__pk=fornecedor_id).order_by('-dataEmissao')
    return render(request, 'certidoes_list.html', {'certidoes':certidoes})

def certidoes_add(request, fornecedor_id):
    fornecedor = models.Fornecedores.objects.get(pk = fornecedor_id)
    # certidoes_form = forms.Certidoes_form(request.POST or None, request.FILES or None)

    CertidoesFormset  = formset_factory(forms.Certidoes_form, extra=0)

    formset = CertidoesFormset (initial=[
        {'tipo':'FGTS', 'autor': request.user, 'fornecedor': fornecedor},
        {'tipo':'FEDERAL', 'autor': request.user, 'fornecedor': fornecedor},
        {'tipo':'ESTADUAL', 'autor': request.user, 'fornecedor': fornecedor},
        {'tipo':'CNDT', 'autor': request.user, 'fornecedor': fornecedor},
        {'tipo':'MUNICIPAL', 'autor': request.user, 'fornecedor': fornecedor}])
    
    
    if request.method == 'POST':
        formset = CertidoesFormset(request.POST, request.FILES)

        # Iterar sobre os formulários individualmente
        for form in formset:
            if form.is_valid():
                form.save()
            else:
                print (f'Erro: {form.errors} / Quantidade: {len(form.errors)}')
        return redirect('dashregularidadefiscal')
            
    return render(request, 'certidoes_add.html', {'certidoes_form':formset, 'fornecedor':fornecedor})

def declaracoes_list(request, fornecedor_id):
    declaracoes = models.Declaracao.objects.filter(fornecedor__pk=fornecedor_id).order_by('-data_emissao')
    return render(request, 'declaracoes_list.html', {'declaracoes':declaracoes})

@login_required
def regularidade_resumo(request, fornecedor_id):
    fornecedor = Fornecedores.objects.get(pk = fornecedor_id)
    return render(request, 'regularidade_resumo.html', {'fornecedor':fornecedor})

def emitir_declaracao(request,fornecedor_id):
    fornecedor = Fornecedores.objects.get(pk = fornecedor_id)
    print(request.POST)
    # Captura a data de referência do formulário
    data_referencia_str = request.POST.get("data_referencia")
    if data_referencia_str:
        data_referencia = datetime.strptime(data_referencia_str, "%Y-%m-%d").date()
    else:
        data_referencia = date.today()

    # Cria a declaração com a data de emissão personalizada
    declaracao = models.Declaracao.objects.create(
        fornecedor=fornecedor,
        emitido_por=request.user,
        data_emissao=data_referencia  # sobrescreve o default do auto_now_add
    )
    certidoes = declaracao.get_certidoes(referencia=data_referencia)

    
    certidao_max = date(2500,1,1)
    certidao_min = date(2000,1,1)
    certidao_none = False
    for tipo, certidao in certidoes.items():
        if certidao:
            if certidao.dataValidade < certidao_max:
                certidao_max = certidao.dataValidade
            if certidao.dataEmissao > certidao_min:
                certidao_min = certidao.dataEmissao
        else:
            certidao_none = True

    declaracao.data_inicio = certidao_min

    if certidao_none:
        declaracao.data_validade = None
    else:
        declaracao.data_validade = certidao_max
        
    # Verifica se todas as certidões foram encontradas
    faltando = [tipo for tipo, certidao in certidoes.items() if certidao is None]

    # Filtra apenas as certidões que não são None
    certidoes_validas = [c for c in certidoes.values() if c is not None]

    # Associa as certidões à declaração
    declaracao.certidoes.set(certidoes_validas)

    # Gerar PDF em bytes
    declaracao_pdf_bytes = gerar_declaracao(request, declaracao, certidoes)

    # Nome do arquivo
    nome_arquivo = f"declaracao_{declaracao.id}.pdf"

    # Atribuir usando ContentFile
    declaracao.arquivo.save(nome_arquivo, ContentFile(declaracao_pdf_bytes))
    if declaracao.data_validade:
        declaracao.situacao = 'regular'
    else:
        declaracao.situacao = 'insuficiente'

    declaracao.save()

    return redirect('dashregularidadefiscal')

# Função para converter imagens em Base64
def encode_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

@login_required
def gerar_declaracao(request, declaracao, certidoes):

    # Função para converter imagens estáticas em Base6
    with open("static/img/bg-timbrado-logo.png", "rb") as image_file:
        page_background = base64.b64encode(image_file.read()).decode('utf-8')

    # Gerar HTML com contexto atualizado
    html_string = render_to_string('declaracao_pdf.html', {
        'page_background': page_background,
        'declaracao': declaracao,
        'certidoes': certidoes,
    })

    # Caminho absoluto do CSS
    base_url = request.build_absolute_uri('/')

    # Gerar o PDF em bytes
    pdf_file = HTML(string=html_string, base_url=base_url).write_pdf()

    return pdf_file

def consulta_externa(request):
    return render(request, 'consultadeclaracao.html')

def dadosdeclaracao_externa(request):
    chave = request.GET.get('chave')
    if not chave:
        messages.error(request, "Chave não informada.")
        return redirect('consulta_externa')
    
    try:
        # Valida se é um UUID válido antes de buscar no banco
        chave_uuid = uuid.UUID(chave)
    except ValueError:
        messages.error(request, "A chave informada não é válida. Verifique e tente novamente.")
        return render(request, 'consultadeclaracao.html', {})

    try:
        declaracao = models.Declaracao.objects.get(codigo=chave)
        certidoes = declaracao.get_certidoes()
        regularidade = all(certidoes.values())
        return render(request, 'dadosdeclaracao_externa.html', {
            'declaracao': declaracao,
            'certidoes': certidoes,
            'regularidade': regularidade,
        })
    except models.Declaracao.DoesNotExist:
        messages.error(request, "Declaração não encontrada ou inválida. Verifique a chave e tente novamente.")
        return redirect('consulta_externa')
    

@login_required
def dashregularidade(request):
    # fornecedor = Fornecedores.objects.get(pk = 1)
    # print(fornecedor)

    # declaracao, certidoes = emitir_declaracao(fornecedor)
    # print(declaracao)
    # print(certidoes)
    return render(request,'dashregularidadefiscal.html', {})




