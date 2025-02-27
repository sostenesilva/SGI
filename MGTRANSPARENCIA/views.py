from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
import pandas as pd
from .models import DbDimensao, DbCriterios, DbAvaliacao, DbAvaliacaoLog
from .forms import AvaliacaoLogForm
from django.core.paginator import Paginator

@login_required
def listar_criterios(request):
    """Lista todas as dimensões e critérios cadastrados."""
    criterios = DbCriterios.objects.select_related('dimensao').all()
    paginator = Paginator(criterios, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listar_criterios.html', {'criterios': page_obj})

@login_required
def listar_avaliacoes(request):
    """Lista as avaliações vinculadas ao usuário logado."""
    avaliacoes = DbAvaliacao.objects.all()
    paginator = Paginator(avaliacoes, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'listar_avaliacoes.html', {'avaliacoes': page_obj})

@login_required
def detalhes_avaliacao(request, avaliacao_id):
    """Exibe detalhes da avaliação e permite o envio de documentos."""
    avaliacao = get_object_or_404(DbAvaliacao, id=avaliacao_id)
    logs = DbAvaliacaoLog.objects.filter(avaliacao=avaliacao).order_by('-data_envio')
    
    return render(request, 'detalhes_avaliacao.html', {
        'avaliacao': avaliacao,
        'logs': logs,
    })


@login_required
def enviar_documento_log(request, log_id):

    avaliacaoLog = get_object_or_404(DbAvaliacaoLog, id=log_id)

    if request.method == 'POST':
        formLog = AvaliacaoLogForm(request.POST, request.FILES, instance=avaliacaoLog)
        if formLog.is_valid():
            log = formLog.save(commit=False)
            log.usuario = request.user
            # log.avaliacao = avaliacaoLog.avaliacao
            log.status = 'Em análise'
            log.save()
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
    log.save()
    return redirect('detalhes_avaliacao', avaliacao_id=log.avaliacao.id)

def apagar_documento_log(request, log_id):
    log = get_object_or_404(DbAvaliacaoLog, id=log_id)
    log.arquivo = None  # Atualiza o status
    log.anotacao = ''  # Atualiza o status
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