from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Demanda, Diligencia
from .forms import DemandaForm, DiligenciaForm
from django.utils import timezone

@login_required
def listar_demandas(request):
    demandas = Demanda.objects.all().order_by('-criada_em')
    return render(request, 'listar_demandas.html', {'demandas': demandas})

@login_required
def criar_demanda(request):
    if request.method == 'POST':
        form = DemandaForm(request.POST)
        if form.is_valid():
            demanda = form.save(commit=False)
            demanda.criada_por = request.user  # <-- Atribui corretamente o usuário
            demanda.save()
            return redirect('listar_demandas')
    else:
        form = DemandaForm()
    return render(request, 'form_demanda.html', {'form': form})

@login_required
def detalhes_demanda(request, demanda_id):
    demanda = get_object_or_404(Demanda, id=demanda_id)
    diligencias = demanda.diligencias.all().order_by('prazo')
    return render(request, 'detalhar_demanda.html', {
        'demanda': demanda,
        'diligencias': diligencias
    })

@login_required
def adicionar_diligencia(request, demanda_id):
    demanda = get_object_or_404(Demanda, id=demanda_id)
    if request.method == 'POST':
        form = DiligenciaForm(request.POST)
        if form.is_valid():
            diligencia = form.save(commit=False)
            diligencia.demanda = demanda
            diligencia.criado_por = request.user
            diligencia.setor_responsavel = request.user.setor_home.first()
            diligencia.save()
            return redirect('detalhar_demanda', demanda_id=demanda.id)
    else:
        form = DiligenciaForm(initial={'demanda': demanda})
    return render(request, 'form_diligencia.html', {
        'form': form,
        'demanda': demanda
    })

@login_required
def editar_demanda(request, demanda_id):
    demanda = get_object_or_404(Demanda, id=demanda_id)
    if request.method == 'POST':
        form = DemandaForm(request.POST, instance=demanda)
        if form.is_valid():
            form.save()
            return redirect('detalhar_demanda', demanda_id=demanda.id)
    else:
        form = DemandaForm(instance=demanda)
    return render(request, 'form_diligencia.html', {
        'form': form,
        'demanda': demanda
    })

@login_required
def excluir_demanda(request, demanda_id):
    demanda = get_object_or_404(Demanda, id=demanda_id)
    if request.method == 'POST':
        demanda.delete()
        return redirect('listar_demandas')
    return render(request, 'confirmar_exclusao.html', {
        'demanda': demanda
    })

@login_required
def editar_diligencia(request, diligencia_id):
    diligencia = get_object_or_404(Diligencia, id=diligencia_id)
    demanda = diligencia.demanda
    if request.method == 'POST':
        form = DiligenciaForm(request.POST, instance=diligencia)
        if form.is_valid():
            form.save()
            return redirect('detalhar_demanda', demanda_id=diligencia.demanda.id)
    else:
        form = DiligenciaForm(instance=diligencia)
    return render(request, 'form_diligencia.html', {
        'form': form,
        'diligencia': diligencia,
        'demanda':demanda
    })

@login_required
def excluir_diligencia(request, diligencia_id):
    diligencia = get_object_or_404(Diligencia, id=diligencia_id)
    demanda = diligencia.demanda
    if request.method == 'POST':
        diligencia.delete()
        return redirect('detalhar_demanda', demanda_id=demanda.id)
    return render(request, 'confirmar_exclusao.html', {
        'diligencia': diligencia
    })
