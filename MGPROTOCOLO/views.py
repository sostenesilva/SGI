import base64
from datetime import datetime
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Prefetch, Q, Case, When, Value, IntegerField, Sum, ExpressionWrapper, F
from django.urls import reverse
from weasyprint import CSS, HTML
from .models import Processo, Documento, Movimentacao, ProtocoloMovimentacao, CorrecaoProcesso, ComprovanteMovimentacao
from HOME.models import Setor
from .forms import ProcessoCorrecaoForm, ProcessoForm, DocumentoForm, MovimentacaoForm, ComprovacaoForm
from django.templatetags.static import static
from django.db.models.functions import Coalesce

@login_required
def processos_no_setor(request):
    """
    Exibe os processos cuja última movimentação está no setor do usuário.
    """
    setor_usuario = request.user.setor_home.all()  # Supondo que o usuário pertence a um setor
    processos = Processo.processos_no_setor(setor_usuario).order_by('-atualizado_em')

    # Capturar o termo de busca
    query = request.GET.get('buscar', '')

    if query:
        processos = processos.filter(
            Q(numero__icontains=query) |
            Q(titulo__icontains=query) |
            Q(demandante__nome__icontains=query) |
            Q(atual__nome__icontains=query) |
            Q(descricao__icontains=query)
        )
    return render(request, 'processos_no_setor.html', {'processos': processos, 'query': query})

@login_required
def processos_encaminhados_pelo_setor(request):
    """
    Exibe os processos que foram encaminhados pelo setor do usuário para outros setores.
    """
    setor_usuario = request.user.setor_home.all()  # Supondo que o usuário pertence a um setor
    processos = Processo.processos_encaminhados_pelo_setor(setor_usuario).order_by('-atualizado_em')
    processos = processos.filter(~Q(atual__sigla='ARQ'))

    # Capturar o termo de busca
    query = request.GET.get('buscar', '')

    if query:
        processos = processos.filter(
            Q(numero__icontains=query) |
            Q(titulo__icontains=query) |
            Q(demandante__nome__icontains=query) |
            Q(atual__nome__icontains=query) |
            Q(descricao__icontains=query)
        )

    return render(request, 'processos_encaminhados_pelo_setor.html', {'processos': processos, 'query': query})

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
            processo.demandante = request.user.setor_home.first()
            processo.atual = request.user.setor_home.first()
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
            for field in form:
                for error in field.errors:
                    messages.error(request, error)
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
        print(request.POST)         
        form = MovimentacaoForm(request.POST, request.FILES)
        if form.is_valid():
            if processo.usuario_pode_modificar(request.user):
                movimentacao = form.save(commit=False)
                movimentacao.processo = processo
                movimentacao.remetente = processo.atual
                movimentacao.realizado_por = request.user
                if movimentacao.destinatario == Setor.objects.get(sigla='ARQ'):
                    movimentacao.status = 'recebida'
                    movimentacao.confirmacao = 'sistema'
                else:
                    movimentacao.status = 'em_tramitacao'
                    movimentacao.confirmacao = 'pendente'
                movimentacao.save()
                
                modalidade_antiga = processo.modalidade
                modalidade_nova = request.POST.get('modalidade')
                if modalidade_antiga != modalidade_nova:
                    CorrecaoProcesso.objects.create(
                            processo=processo,
                            usuario=request.user,
                            campo_alterado='modalidade',
                            valor_anterior=modalidade_antiga,
                            valor_novo=modalidade_nova
                        )
                    processo.modalidade = modalidade_nova
                    processo.save()
                elif modalidade_antiga == modalidade_nova:
                    pass
                else:
                    messages.error(request, "Escolha uma modalidade válida.")
    
            return redirect('detalhes_processo', processo_id=processo.id)
    else:
        form = MovimentacaoForm(initial={
            'processo': processo,
            'remetente': processo.atual
        })
    return render(request, 'criar_movimentacao.html', {'form': form, 'processo': processo})

@login_required
def listar_movimentacoes_tramitacao(request):
    setores_usuario = request.user.setor_home.all()

    if not setores_usuario.exists():
        return render(request, 'listar_movimentacoes_tramitacao.html', {'setores': []})

    setores_ids = setores_usuario.values_list('id', flat=True)

    # Prefetch dos setores DESTINATÁRIOS com movimentações PENDENTES feitas por setores do usuário
    setores = Setor.objects.prefetch_related(
        Prefetch(
            'SetorDestinatario',  # related_name da FK `destinatario` na model Movimentacao
            queryset=Movimentacao.objects.filter(
                remetente__in=setores_ids,
                status='em_tramitacao',
                confirmacao='pendente'
            ).select_related('remetente', 'destinatario', 'processo'),
            to_attr='movs_pendentes'
        )
    ).filter(SetorDestinatario__remetente__in=setores_ids).distinct()

    return render(request, 'listar_movimentacoes_tramitacao.html', {'setores': setores})


@login_required
def gerar_protocolo(request):

    if request.method == 'POST':
        movimentacoes_ids = request.POST.getlist('movimentacoes')
        movimentacoes = Movimentacao.objects.filter(id__in=movimentacoes_ids)

        if movimentacoes.exists():
            # Verificar se todas as movimentações são do mesmo setor de destino
            SetorDestinatario = movimentacoes.first().destinatario
            if not all(m.destinatario == SetorDestinatario for m in movimentacoes):
                messages.error(request, "Todas as movimentações devem ser do mesmo setor de destino.")
                return redirect('listar_movimentacoes_tramitacao')  # ou a view da página anterior

            # Criar o protocolo
            protocolo = ProtocoloMovimentacao.objects.create(
                destinatario=SetorDestinatario,
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
                'setor_usuario': request.user.setor_home.first()
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
def arquivar_processo(request, processo_id):
    processo = get_object_or_404(Processo, id=processo_id)
    arquivo = get_object_or_404(Setor, sigla='ARQ')

    # Verifica se o processo já está arquivado ou concluído
    if processo.status in ['arquivado', 'concluido', 'cancelado']:
        return redirect('processos_no_setor')

    # Criar movimentação de arquivamento
    movimentacao = Movimentacao.objects.create(
        processo=processo,
        descricao=f"Processo arquivado pelo setor {processo.atual}",
        realizado_por=request.user,
        remetente=processo.atual,  # Último setor que estava
        destinatario=arquivo,  # Não há destino real
        status='arquivada',
        confirmado_em = datetime.now(),
        realizado_em = datetime.now(),
    )

    # Alterar status do processo para arquivado
    processo.status = 'arquivado'
    processo.atual = arquivo  # Remove o setor atual, pois foi arquivado
    processo.ultima_movimentacao = movimentacao  # Atualiza a última movimentação
    processo.save()

    return redirect('processos_no_setor')


@login_required
def listar_protocolos(request):
    setores_usuario = request.user.setor_home.all()
    protocolos = ProtocoloMovimentacao.objects.filter(criado_por = request.user).order_by('-criado_em')
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
    setor_usuario = request.user.setor_home.all()
    ultima_movimentacao = processo.ultima_movimentacao

    if ultima_movimentacao and ultima_movimentacao.destinatario in setor_usuario:
        ultima_movimentacao.status = 'recebida'
        ultima_movimentacao.confirmacao = 'sistema'
        ultima_movimentacao.confirmado_por = request.user
        ultima_movimentacao.confirmado_em = datetime.now()
        ultima_movimentacao.save()
    
    return redirect('processos_no_setor')

@login_required
def processos_arquivados(request):
    setor_usuario = request.user.setor_home.all()

    processos = Processo.objects.filter(atual__sigla='ARQ')

    # Capturar o termo de busca
    query = request.GET.get('buscar', '')

    if query:
        processos = processos.filter(
            Q(numero__icontains=query) |
            Q(titulo__icontains=query) |
            Q(demandante__nome__icontains=query) |
            Q(atual__nome__icontains=query) |
            Q(descricao__icontains=query)
        )

    # Converte para lista ou mantém como QuerySet
    processos_filtrados = []
    for processo in processos:
        setores_env = processo.setores_envolvidos()  # retorna lista de nomes
        # Checa se o nome de algum setor do usuário está nos setores envolvidos
        if any(setor.nome in setores_env for setor in setor_usuario):
            processos_filtrados.append(processo)
    
    return render(request, 'processos_arquivados.html', {'processos': processos_filtrados, 'query': query })

@login_required
def mais_informacoes(request, processo_id):
    processo = Processo.objects.get(pk = processo_id)
    return render(request, 'mais_informacoes.html', {'processo' : processo})

@login_required
def historico_correcoes_processo(request, processo_id):
    processo = get_object_or_404(Processo, id=processo_id)
    correcoes = processo.correcoes.order_by('-data')
    form = ProcessoCorrecaoForm(instance=processo, disabled =not processo.usuario_pode_modificar(request.user))
    pode_modificar = processo.usuario_pode_modificar(request.user)
    context = {
        'processo': processo,
        'correcoes': correcoes,
        'form': form,
        'pode_modificar':pode_modificar
    }
    return render(request, 'correcao_processo_modal.html', context)

@login_required
def salvar_correcoes_processo(request, processo_id):
    processo = get_object_or_404(Processo, id=processo_id)

    if request.method == 'POST':
        form = ProcessoCorrecaoForm(request.POST, instance=processo)

        # 🔸 Capture os valores antigos *antes* de atualizar o processo
        valores_anteriores = {
            'numero': processo.numero,
            'titulo': processo.titulo,
            'descricao': processo.descricao,
            'fim':processo.fim,
            'modalidade': processo.modalidade
        }

        if form.is_valid():
            for field in valores_anteriores:
                antigo = valores_anteriores[field]
                novo = form.cleaned_data.get(field)

                if antigo != novo:
                    CorrecaoProcesso.objects.create(
                        processo=processo,
                        usuario=request.user,
                        campo_alterado=field,
                        valor_anterior=antigo,
                        valor_novo=novo
                    )
            form.save()
            return HttpResponse(
                headers={"HX-Redirect": reverse("detalhes_processo", args=[processo.id])}
            )


@login_required
def sugerir_descricao_processo(request):
    descricao_digitada = request.GET.get('descricao', '').strip()
    termos = descricao_digitada.lower().split()

    if not termos:
        return render(request, 'sugestao_processo.html', {'sugestoes': []})

    # Filtro: qualquer termo no título, descrição ou número
    filtro_q = Q()
    for termo in termos:
        filtro_q |= Q(descricao__icontains=termo) | Q(titulo__icontains=termo) | Q(numero__icontains=termo)

    # Soma da pontuação de relevância
    relevancia = None
    for termo in termos:
        partes = [
            Case(When(descricao__icontains=termo, then=Value(1)), default=Value(0), output_field=IntegerField()),
            Case(When(titulo__icontains=termo, then=Value(1)), default=Value(0), output_field=IntegerField()),
            Case(When(numero__icontains=termo, then=Value(1)), default=Value(0), output_field=IntegerField())
        ]
        for parte in partes:
            relevancia = parte if relevancia is None else relevancia + parte

    processos = Processo.objects.filter(filtro_q)\
        .annotate(relevancia=ExpressionWrapper(relevancia, output_field=IntegerField()))\
        .order_by('-relevancia', '-criado_em')[:5]

    return render(request, 'sugestao_processo.html', {'sugestoes': processos})


@login_required
def gerar_historico_tramitacoes(request, processo_id):

    processo = Processo.objects.get(id = processo_id)
    movimentacoes = processo.movimentacoes.all()
    comprovante = ComprovanteMovimentacao.objects.create(
        criado_por = request.user
    )
    comprovante.movimentacoes.set(movimentacoes)
    comprovante.save()
    # Função para converter imagens estáticas em Base6
    with open("static/img/bg-timbrado-logo.png", "rb") as image_file:
        page_background = base64.b64encode(image_file.read()).decode('utf-8')

    # Gerar HTML com contexto atualizado
    html_string = render_to_string('tramitacoes_pdf.html', {
        'processo': processo,
        'movimentacoes': movimentacoes,
        'comprovante': comprovante,
        'page_background': page_background,
    })

    # Caminho absoluto do CSS
    base_url = request.build_absolute_uri('/')

    # Gerar PDF
    pdf_file = HTML(string=html_string, base_url=base_url).write_pdf()

    # Retornar o PDF para download
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Tramitacoes do Processo {processo.id}.pdf"'
    return response
