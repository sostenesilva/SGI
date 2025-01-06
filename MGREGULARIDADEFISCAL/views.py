import os
from django.shortcuts import redirect, render
from datetime import date
from weasyprint import CSS, HTML
from docx import Document
import pypandoc
from python_docx_replace import docx_replace
import base64
from SGI import settings
from . import models, forms
from django.forms import formset_factory, modelformset_factory
from MGC.models import Fornecedores
from django.template.loader import render_to_string

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
    declaracoes = models.Declaracao.objects.filter(fornecedor__pk=fornecedor_id)
    return render(request, 'declaracoes_list.html', {'declaracoes':declaracoes})

def regularidade_resumo(request, fornecedor_id):
    fornecedor = Fornecedores.objects.get(pk = fornecedor_id)
    return render(request, 'regularidade_resumo.html', {'fornecedor':fornecedor})

def emitir_declaracao(request,fornecedor_id):
    fornecedor = Fornecedores.objects.get(pk = fornecedor_id)
    declaracao = models.Declaracao.objects.create(fornecedor=fornecedor)
    certidoes = declaracao.get_certidoes()

    # Verifica se todas as certidões foram encontradas
    faltando = [tipo for tipo, certidao in certidoes.items() if certidao is None]
    
    print(certidoes)

    if faltando:
        print(f"Certidões faltando: {', '.join(faltando)}")

    ver_declaracao(request,declaracao)

    return redirect('dashregularidadefiscal')

# Função para converter imagens em Base64
def encode_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def ver_declaracao (request, declaracao):

    header_image = encode_image_base64("static/img/header.png")
    footer_image = encode_image_base64("static/img/footer.png")
    brasao_image = encode_image_base64("static/img/logo-horizontal.png")

    certidoes_html=""
    certidao_max = date(2500,1,1)
    certidao_min = date(2000,1,1)

    for tipo, certidao in declaracao.get_certidoes().items():
        if certidao:
            if certidao.dataValidade < certidao_max:
                certidao_max = certidao.dataValidade
            if certidao.dataEmissao > certidao_min:
                certidao_min = certidao.dataEmissao


            certidoes_html += f"""
            <tr>
                <td>{tipo}</td>
                <td>{certidao.dataEmissao.strftime('%d/%m/%Y')}</td>
                <td>{certidao.dataValidade.strftime('%d/%m/%Y')}</td>
                <td>{certidao.autenticacao}</td>
            </tr>"""

    template = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Declaração de Conformidade Fiscal</title>
    </head>
    <link rel="stylesheet" href="static/css/detail_pdf_gen.css">
        <style>
            header {{
                background-image: url("data:image/png;base64,{header_image}");
            }}

            footer {{
                background-image: url("data:image/png;base64,{footer_image}");
            }}
        </style>
    <body>
        <header>
        <img class="brasao" src="data:image/png;base64,{brasao_image}" alt="Brasão da Prefeitura">
        </header>

            <!-- Conteúdo Principal -->
        <div class="content">
            <h1 style="text-align: center;">Declaração de Conformidade Fiscal</h1>
            <p>Emitimos a presente Declaração de Conformidade Fiscal, confirmando que o fornecedor abaixo identificado atende aos requisitos de regularidade fiscal, conforme documentação apresentada e validada por esta administração pública.</p>
            <p style="margin:0; padding:0;"><strong>Fornecedor:</strong> {declaracao.fornecedor.RazaoSocial}</p>
            <p style="margin:0; padding:0;"><strong>CNPJ/CPF:</strong> {declaracao.fornecedor.NumeroDocumentoAjustado}</p>
            <p style="margin:0; padding:0;"><strong>Vigência: </strong> {certidao_min.strftime('%d/%m/%Y')} à {certidao_max.strftime('%d/%m/%Y')}</p>

            <h2 class="section-title">Certidões</h2>
            <table>
                <thead>
                    <tr>
                        <th>Certidão</th>
                        <th>Data de Emissão</th>
                        <th>Data de Validade</th>
                        <th>Autenticação</th>
                    </tr>
                </thead>
                <tbody>
        """
    
    template += certidoes_html

    template += f"""</tbody>
                </table>
                <h2 class="section-title">Instruções para Validação</h2>
                <p style="margin:0px">Esta declaração possui uma chave de autenticidade, que permite a consulta online das certidões associadas e de sua validade. Para verificar esta declaração, acesse o site: <strong>https://cortes.sginformacao.com.br/regularidadefiscal/consultar</strong></p>
                <p>Chave de autenticação: <strong>{declaracao.codigo}</strong></p>
                <p><strong>Observações Importantes:</strong></p>
                <ul>
                    <li>A validade desta declaração está condicionada à vigência das certidões apresentadas.</li>
                    <li>Documento gerado eletronicamente por meio do sistema de gestão da informação. Qualquer alteração ou modificação invalida este documento.</li>
                    <li>Em caso de inconsistências ou dúvidas, entre em contato com o setor responsável.</li>
                </ul>
            </div>

            <footer><div class="dados-footer">
            <p style="margin:0px">Rua Coronel José Belarmino, nº 048, Centro, Cortês-PE</p>                    
            <p style="margin:0px">CEP 55.525-000 | CNPJ: 10.273.548/0001-69</p>
            <p style="margin:0px">E-mail: gabineteprefeitacortes@gmail.com</p>
            </div>
            </footer>
        </body>
        </html>"""
    
    caminho_pdf = f'media/MGREGULARIDADEFISCAL/declaracoes/{declaracao.codigo}.pdf'

    base_url = os.path.dirname(os.path.realpath(__file__))+"/"
    html = HTML(string=template, base_url=base_url)
    css = CSS("./static/css/detail_pdf_gen.css", base_url=base_url)

    html.write_pdf(caminho_pdf, stylesheets=[css])

    # HTML(string=template, base_url=request.build_absolute_uri('/')).write_pdf(caminho_pdf,  stylesheets=[CSS('static/css/detail_pdf_gen.css')],  presentational_hints=True)
    return html

    




def dashregularidade(request):
    # fornecedor = Fornecedores.objects.get(pk = 1)
    # print(fornecedor)

    # declaracao, certidoes = emitir_declaracao(fornecedor)
    # print(declaracao)
    # print(certidoes)
    return render(request,'dashregularidadefiscal.html', {})




