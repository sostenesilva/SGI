import base64
from datetime import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch
from weasyprint import CSS, HTML
from .models import Processo, Documento, Movimentacao, ProtocoloMovimentacao, Setor
from .forms import ProcessoForm, DocumentoForm, MovimentacaoForm, ComprovacaoForm
from django.templatetags.static import static

@login_required
def processos_no_setor(request):
    """
    Exibe os processos cuja última movimentação está no setor do usuário.
    """
    setor_usuario = request.user.setores.first()  # Supondo que o usuário pertence a um setor
    processos = Processo.processos_no_setor(setor_usuario)
    return render(request, 'processos_no_setor.html', {'processos': processos})

@login_required
def processos_encaminhados_pelo_setor(request):
    """
    Exibe os processos que foram encaminhados pelo setor do usuário para outros setores.
    """
    setor_usuario = request.user.setores.first()  # Supondo que o usuário pertence a um setor
    processos = Processo.processos_encaminhados_pelo_setor(setor_usuario)
    return render(request, 'processos_encaminhados_pelo_setor.html', {'processos': processos})

@login_required
def detalhes_processo(request, processo_id):
    """
    Exibe os detalhes de um processo específico.
    """
    processo = get_object_or_404(Processo, id=processo_id)
    pode_modificar = processo.usuario_pode_modificar(request.user)

    return render(request, 'detalhes_processo.html', {'processo': processo, 'pode_modificar': pode_modificar})

@login_required
def criar_processo(request):
    if request.method == 'POST':
        form = ProcessoForm(request.POST, request.FILES)
        if form.is_valid():
            processo = form.save(commit=False)
            processo.criado_por = request.user
            processo.setor_demandante = request.user.setores.first()
            processo.setor_atual = request.user.setores.first()
            processo.save()

            # Salvar documentos iniciais
            documentos_iniciais = request.FILES.getlist('documentos_iniciais')  # Recebe múltiplos arquivos
            for arquivo in documentos_iniciais:
                Documento.objects.create(
                    processo=processo,
                    descricao=f"Documento Inicial - {arquivo.name}",
                    classificacao='outros',
                    tipo='inicial',
                    arquivo=arquivo,
                    criado_por=request.user
                )

            return redirect('detalhes_processo', processo_id=processo.id)
    else:
        form = ProcessoForm()
    return render(request, 'criar_processo.html', {'form': form})

@login_required
def editar_processo(request, processo_id):
    processo = get_object_or_404(Processo, id=processo_id)
    if request.method == 'POST':
        form = ProcessoForm(request.POST, instance=processo)
        if form.is_valid():
            form.save()
            return redirect('detalhes_processo', processo_id=processo.id)
    else:
        form = ProcessoForm(instance=processo)
    return render(request, 'editar_processo.html', {'form': form})

@login_required
def criar_documento(request, processo_id):
    processo = get_object_or_404(Processo, id=processo_id)
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.processo = processo
            documento.criado_por = request.user 
            documento.tipo = 'complementar'
            documento.save()
            return redirect('detalhes_processo', processo_id=processo.id)
    else:
        form = DocumentoForm()
    return render(request, 'criar_documento.html', {'form': form, 'processo': processo})

@login_required
def criar_movimentacao(request, processo_id):
    processo = get_object_or_404(Processo, id=processo_id)
    if request.method == 'POST':
        form = MovimentacaoForm(request.POST, request.FILES)
        if form.is_valid():
            movimentacao = form.save(commit=False)
            movimentacao.processo = processo
            movimentacao.setor_origem = processo.setor_atual
            movimentacao.status = 'em_tramitacao'
            movimentacao.confirmacao = 'pendente'
            movimentacao.realizado_por = request.user
            movimentacao.save()
            return redirect('detalhes_processo', processo_id=processo.id)
    else:
        form = MovimentacaoForm(initial={
            'processo': processo,
            'setor_origem': processo.setor_atual
        })
    return render(request, 'criar_movimentacao.html', {'form': form, 'processo': processo})

@login_required
def listar_movimentacoes_tramitacao(request):
    usuario = request.user
    setor_usuario = usuario.setores.first()  # Supondo que o usuário pertence a apenas um setor

    if not setor_usuario:
        return render(request, 'listar_movimentacoes_tramitacao.html', {'setores': []})

    # Filtrar apenas movimentações enviadas pelo setor do usuário logado
    setores = Setor.objects.prefetch_related(
        Prefetch(
            'movimentacoes_destino',
            queryset=Movimentacao.objects.filter(
                setor_origem=setor_usuario,  # Movimentações enviadas pelo setor do usuário
                status='em_tramitacao',
                confirmacao='pendente'
            )
        )
    ).distinct()

    return render(request, 'listar_movimentacoes_tramitacao.html', {'setores': setores})


@login_required
def gerar_protocolo(request):

    if request.method == 'POST':
        movimentacoes_ids = request.POST.getlist('movimentacoes')
        movimentacoes = Movimentacao.objects.filter(id__in=movimentacoes_ids)

        if movimentacoes.exists():
            # Verificar se todas as movimentações são do mesmo setor de destino
            setor_destino = movimentacoes.first().setor_destino
            if not all(m.setor_destino == setor_destino for m in movimentacoes):
                return HttpResponse("Todas as movimentações devem ser do mesmo setor de destino.", status=400)

            # Criar o protocolo
            protocolo = ProtocoloMovimentacao.objects.create(
                setor_destino=setor_destino,
                criado_por=request.user
            )
            protocolo.movimentacoes.set(movimentacoes)

            # Atualizar status das movimentações
            movimentacoes.update(confirmacao='manual')

            # Função para converter imagens estáticas em Base6
            with open("static/img/bg-timbrado-logo.png", "rb") as image_file:
                page_background = base64.b64encode(image_file.read()).decode('utf-8')

            # Gerar HTML com contexto atualizado
            html_string = render_to_string('protocolo_pdf.html', {
                'protocolo': protocolo,
                'page_background': page_background,
            })

            # Caminho absoluto do CSS
            base_url = request.build_absolute_uri('/')

            # Gerar PDF
            pdf_file = HTML(string=html_string, base_url=base_url).write_pdf()

            # Retornar o PDF para download
            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="protocolo_{protocolo.id}.pdf"'
            return response

    return redirect('listar_movimentacoes_tramitacao')

@login_required
def listar_protocolos(request):
    protocolos = ProtocoloMovimentacao.objects.all()
    return render(request, 'listar_protocolos.html', {'protocolos': protocolos})

@login_required
def anexar_comprovacao(request, protocolo_id):
    protocolo = get_object_or_404(ProtocoloMovimentacao, id=protocolo_id)
    if request.method == 'POST':
        form = ComprovacaoForm(request.POST, request.FILES, instance=protocolo)
        if form.is_valid():
            protocolo = form.save()
            protocolo.confirmar()  # Atualiza o status do protocolo e das movimentações
            return redirect('listar_protocolos')
    else:
        form = ComprovacaoForm(instance=protocolo)
    return render(request, 'anexar_comprovacao.html', {'form': form, 'protocolo': protocolo})

@login_required
def visualizar_comprovacao(request, protocolo_id):
    protocolo = get_object_or_404(ProtocoloMovimentacao, id=protocolo_id)
    return render(request, 'visualizar_comprovacao.html', {'protocolo': protocolo})

@login_required
def receber_processo(request, processo_id):
    processo = get_object_or_404(Processo, id=processo_id)
    
    # Verifica se o usuário pertence ao setor atual
    setor_usuario = request.user.setores.first()
    ultima_movimentacao = processo.ultima_movimentacao

    if ultima_movimentacao and ultima_movimentacao.setor_destino == setor_usuario:
        ultima_movimentacao.status = 'recebida'
        ultima_movimentacao.confirmacao = 'sistema'
        ultima_movimentacao.confirmado_por = request.user
        ultima_movimentacao.confirmado_em = datetime.now()
        ultima_movimentacao.save()
    
    return redirect('processos_no_setor')