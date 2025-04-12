from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
from .models import DbDimensao, DbCriterios, DbAvaliacao, DbAvaliacaoLog, InformacoesCriterio
from .forms import AvaliacaoLogForm, AvaliacaoForm
from django.core.paginator import Paginator
from HOME.models import Secretaria, Setor
from django.db.models import Q
from HOME.utils import notificar


@login_required
def listar_criterios(request):
    """Lista todas as dimensões e critérios cadastrados."""
    criterios = DbCriterios.objects.select_related('dimensao').all()
    paginator = Paginator(criterios, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listar_criterios.html', {'criterios': criterios})

@login_required
def listar_avaliacoes(request):
    """Lista as avaliações vinculadas ao usuário logado."""

    if Setor.objects.get(sigla='CSCI').usuarios.contains(request.user):
        avaliacoes = DbAvaliacao.objects.all()
    else:
        avaliacoes = DbAvaliacao.objects.filter(secretaria__setores__in=request.user.setor_home.all())

    # Capturar o termo de busca
    query = request.GET.get('buscar', '')

    if query:
        avaliacoes = avaliacoes.filter(
            Q(criterio__item__icontains=query) |
            Q(criterio__criterio__icontains=query) |
            Q(criterio__dimensao__dimensao__icontains=query) |
            Q(criterio__periodicidade__icontains=query) |
            Q(criterio__classificacao__icontains=query) |
            Q(secretaria__nome__icontains=query) |
            Q(secretaria__sigla__icontains=query) |
            Q(status__icontains=query)
        )

    paginator = Paginator(avaliacoes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listar_avaliacoes.html', {'avaliacoes': avaliacoes, 'query': query})

@login_required
def detalhes_avaliacao(request, avaliacao_id):
    """Exibe detalhes da avaliação e permite o envio de documentos."""
    avaliacao = get_object_or_404(DbAvaliacao, id=avaliacao_id)
    logs = DbAvaliacaoLog.objects.filter(avaliacao=avaliacao).order_by('-data_limite')
    
    return render(request, 'detalhes_avaliacao.html', {
        'avaliacao': avaliacao,
        'logs': logs,
    })


@login_required
def enviar_documento_log(request, log_id):

    avaliacaoLog = get_object_or_404(DbAvaliacaoLog, id=log_id)
    controle = get_object_or_404(Secretaria, sigla='SCI')

    if request.method == 'POST':
        formLog = AvaliacaoLogForm(request.POST, request.FILES, instance=avaliacaoLog)
        if formLog.is_valid():
            log = formLog.save(commit=False)
            log.usuario = request.user
            log.status = 'Em análise'
            log.data_envio = datetime.now()
            log.save()
            
            for usuarioControle in controle.usuarios.all():
                notificar(usuarioControle,f'Novo documento enviado por {request.user}',f'O usuário {request.user} enviou em um documento sobre "{avaliacaoLog.tarefa}" no critério {avaliacaoLog.avaliacao.criterio.item}')
            
            return redirect('detalhes_avaliacao', avaliacao_id=avaliacaoLog.avaliacao.id)
    else:
        formLog = AvaliacaoLogForm()

    return render(request, 'enviar_documento.html', {
        'form': formLog,
        'log':avaliacaoLog
    })


# 🔹 ATUALIZAR STATUS DO ENVIO (aprovado ou rejeitado)
@login_required
def atualizar_status_log(request, log_id, status):
    log = get_object_or_404(DbAvaliacaoLog, id=log_id)
    if request.user.has_perm('controle_transparencia'):
        log.status = status
        log.save()
    return redirect('detalhes_avaliacao', avaliacao_id=log.avaliacao.id)


def aprovar_documento(request, log_id):
    log = get_object_or_404(DbAvaliacaoLog, id=log_id)
    log.status = "Publicado"  # Atualiza o status
    log.data_publicacao = datetime.now()
    log.save()
    return redirect('detalhes_avaliacao', avaliacao_id=log.avaliacao.id)

def apagar_documento_log(request, log_id):
    log = get_object_or_404(DbAvaliacaoLog, id=log_id)
    log.arquivo = None  # Atualiza o status
    log.anotacao = ''  # Atualiza o status
    log.status = 'Pendente'  # Atualiza o status
    log.save()
    return redirect('detalhes_avaliacao', avaliacao_id=log.avaliacao.id)


@login_required
def importar_criterios(request):
    
    if request.POST:
        dataframe = pd.read_excel(request.FILES.get('criterios'))
        for index, row in dataframe.iterrows():
            if row[0] == 'PODER EXECUTIVO' or row[0] == 'COMUM':
                criterioadd = DbCriterios.objects.create(
                    item = str(row[2]),
                    criterio = str(row[3]),
                    # dimensao = row[1],
                    classificacao = str(row[4])
                )
                criterioadd.save()

    return render(request, 'add_criterios.html')

@login_required
def adicionar_avaliacao(request):

    if request.method == 'POST':
        formAval = AvaliacaoForm(request.POST)
        if formAval.is_valid():
            aval = formAval.save(commit=False)
            # log.usuario = request.user
            # log.avaliacao = avaliacaoLog.avaliacao
            # log.status = 'Em análise'
            aval.save()
            print('aval salvo')
            data_limite = request.POST.get('data_limite')  # Captura o valor do input
            print(data_limite)
            
            if data_limite:
                DbAvaliacaoLog.objects.create(
                    avaliacao=aval,
                    data_limite=data_limite,
                    status='Pendente',
                )
                print('criado!')
            return redirect('detalhes_avaliacao', avaliacao_id=aval.id)
    else:
        formAval = AvaliacaoForm()
        return render(request, 'criar_avaliacao.html', {
            'formAval': formAval,
        })
    
@login_required
def adicionar_tarefa(request, avaliacao_id):

    avaliacao = get_object_or_404(DbAvaliacao, id=avaliacao_id)

    if request.method == 'POST':
        data_limite = request.POST.get('data_limite')  # Captura o valor do input
        tarefa_descricao = request.POST.get('tarefa')  # Captura o valor do input
        if data_limite:
            DbAvaliacaoLog.objects.create(
                avaliacao=avaliacao,
                tarefa=tarefa_descricao,
                data_limite=data_limite,
                status='Pendente',
            )
            return redirect('detalhes_avaliacao', avaliacao_id = avaliacao.id)

    return render(request, 'add_tarefa.html', {
        'avaliacao': avaliacao,
    })

@login_required
def editar_tarefa(request, tarefa_id):

    tarefa = get_object_or_404(DbAvaliacaoLog, id=tarefa_id)

    if request.method == 'POST':
        data_limite = request.POST.get('data_limite')  # Captura o valor do input
        tarefa_descricao = request.POST.get('tarefa')  # Captura o valor do input
        if data_limite:
            tarefa.data_limite = data_limite
            tarefa.tarefa = tarefa_descricao
            tarefa.save()
            return redirect('detalhes_avaliacao', avaliacao_id = tarefa.avaliacao.id)

    return render(request, 'editar_tarefa.html', {
        'tarefa': tarefa,
    })

@login_required
def informacoes_criterios(request, criterio_id):
    criterio = DbCriterios.objects.get(id = criterio_id)
    informacoes = InformacoesCriterio.objects.filter(Q(criterio = criterio) | Q(geral = True))
    return render(request, 'Info_criterio.html', {'informacoes': informacoes})


def atualizar_criterios():
    criterios = DbCriterios.objects.all()
    dataframe = pd.read_excel('MGTRANSPARENCIA\matriz.xlsx')
    iguais = 0
    dif = 0
    crit = 0
    for index, row in dataframe.iterrows():
        crit += 1
        for criterio in criterios:
            if row[3] == criterio.criterio:
                # print(row[3])
                iguais += 1
                break
        # print(row[3])
        dif += 1
    print(f'Critérios: {crit} | Iguais: {iguais} | Diferentes: {dif}')
    return print('fim')