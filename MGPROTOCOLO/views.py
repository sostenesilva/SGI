from datetime import datetime
from django.shortcuts import get_object_or_404, render, redirect
from .models import Documento, Setor, Movimentacao, ProtocoloMovimentacao
from .forms import DocumentoForm
from django.db.models import Q
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.http import HttpResponse
from django.db.models import Max

def registrar_documento(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_documentos')
    else:
        form = DocumentoForm()

    return render(request, 'registrar_documento.html', {'form': form})

def listar_documentos(request):
    documentos = Documento.objects.all()

    # Filtros
    status = request.GET.get('status')
    tipo = request.GET.get('tipo')
    if status:
        documentos = documentos.filter(status=status)
    if tipo:
        documentos = documentos.filter(tipo=tipo)

    return render(request, 'listar_documentos.html', {'documentos': documentos})

def registrar_movimentacao(request, documento_id):
    documento = Documento.objects.get(id=documento_id)

    if request.method == 'POST':
        destino = request.POST.get('destino')
        observacao = request.POST.get('observacao')

        Movimentacao.objects.create(
            documento=documento,
            origem=documento.origem,
            destino=Setor.objects.get(id=destino),
            usuario=request.user,
            observacao=observacao
        )
        documento.status = 'Em Tramitação'
        documento.save()

        return redirect('listar_documentos')

    setores = Setor.objects.exclude(id=documento.origem.id)
    return render(request, 'registrar_movimentacao.html', {'documento': documento, 'setores': setores})

def concluir_documento(request, documento_id):
    documento = Documento.objects.get(id=documento_id)
    documento.status = 'Concluído'
    documento.data_conclusao = datetime.now()
    documento.save()
    return redirect('listar_documentos')

def consultar_movimentacao(request):
    query = request.GET.get('query', '')  # Texto buscado pelo usuário
    movimentacoes = Movimentacao.objects.all()

    if query:
        # Busca por título, origem ou destino
        movimentacoes = movimentacoes.filter(
            Q(documento__titulo__icontains=query) |
            Q(origem__nome__icontains=query) |
            Q(destino__nome__icontains=query)
        )

    return render(request, 'consultar_movimentacao.html', {
        'movimentacoes': movimentacoes,
        'query': query,
    })

def emitir_relatorio_protocolo(request):
    if request.method == 'POST':
        # Obtém IDs das movimentações selecionadas
        movimentacao_ids = request.POST.getlist('movimentacoes')
        movimentacoes = Movimentacao.objects.filter(id__in=movimentacao_ids)

        # Renderiza o HTML para o PDF
        template = render_to_string('sei/relatorio_protocolo.html', {
            'movimentacoes': movimentacoes,
            'data_emissao': datetime.now(),
        })

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="relatorio_protocolo.pdf"'

        HTML(string=template).write_pdf(response)
        return response

    # Se não houver movimentações selecionadas, redireciona para listagem
    return redirect('listar_documentos')

def upload_relatorio(request, relatorio_id):
    # Obtém o documento correspondente ao relatório
    documento = get_object_or_404(Documento, id=relatorio_id)

    if request.method == 'POST':
        # Recebe o arquivo enviado pelo usuário
        arquivo = request.FILES.get('arquivo')
        if arquivo:
            # Atribui o arquivo diretamente ao campo de arquivo no modelo
            documento.arquivo = arquivo
            documento.status = 'Concluído'
            documento.data_conclusao = datetime.now()
            documento.save()

            # Atualiza as movimentações associadas
            documento.movimentacoes.update(observacao='Aprovado pelo upload do relatório')

            return redirect('listar_documentos')
        else:
            return render(request, 'upload_relatorio.html', {
                'relatorio': documento,
                'error': 'Por favor, envie um arquivo válido.',
            })

    return render(request, 'upload_relatorio.html', {'relatorio': documento})



def listar_movimentacoes_em_tramitacao(request):
    movimentacoes = Movimentacao.objects.filter(documento__status="Em Tramitação")
    setores = Setor.objects.all()

    if request.method == 'POST':
        # Obter IDs das movimentações selecionadas
        movimentacoes_ids = request.POST.getlist('movimentacoes')
        destino_id = request.POST.get('destino')

        if movimentacoes_ids and destino_id:
            # Gerar um número de protocolo
            ultimo_protocolo = ProtocoloMovimentacao.objects.aggregate(Max('id'))['id__max'] or 0
            numero_protocolo = f"PM-{ultimo_protocolo + 1:04d}-{datetime.now().year}"

            # Criar o protocolo
            protocolo = ProtocoloMovimentacao.objects.create(
                numero=numero_protocolo,
                destino_id=destino_id,
            )
            protocolo.movimentacoes.set(Movimentacao.objects.filter(id__in=movimentacoes_ids))
            protocolo.save()

            return redirect('emitir_protocolo', protocolo_id=protocolo.id)

    return render(request, 'listar_movimentacoes_em_tramitacao.html', {
        'movimentacoes': movimentacoes,
        'setores': setores,
    })

def emitir_protocolo(request, protocolo_id):
    protocolo = ProtocoloMovimentacao.objects.get(id=protocolo_id)

    # Renderizar o PDF
    template = render_to_string('protocolo_pdf.html', {'protocolo': protocolo})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="Protocolo_{protocolo.numero}.pdf"'

    HTML(string=template).write_pdf(response)
    return response

def listar_protocolos_pendentes(request):
    protocolos = ProtocoloMovimentacao.objects.filter(status="Pendente")
    return render(request, 'listar_protocolos_pendentes.html', {'protocolos': protocolos})

def finalizar_protocolo(request, protocolo_id):
    protocolo = ProtocoloMovimentacao.objects.get(id=protocolo_id)

    if request.method == 'POST':
        arquivo = request.FILES.get('arquivo_assinado')
        if arquivo:
            protocolo.arquivo_assinado = arquivo
            protocolo.status = "Finalizado"
            protocolo.save()

            # Atualizar o status das movimentações
            protocolo.movimentacoes.update(status="Concluído")

            return redirect('sei:listar_protocolos_pendentes')

    return render(request, 'sei/finalizar_protocolo.html', {'protocolo': protocolo})



