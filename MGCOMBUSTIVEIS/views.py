from datetime import date, timedelta
import json
from django.http import HttpResponse
from django.shortcuts import render
from . import models, forms
from django.core.paginator import Paginator
from . import models
from django.db.models import Count, Sum



def dashcombustiveis(request):
    
    # Resumo geral
    total_veiculos = models.veiculo.objects.count()
    total_condutores = models.condutor.objects.count()
    total_abastecimentos = models.Abastecimentos.objects.count()

    # Gráficos
    veiculos_secretaria = models.veiculo.objects.values('secretaria').annotate(total=Count('id'))
    veiculos_secretaria_labels = [v['secretaria'] for v in veiculos_secretaria]
    veiculos_secretaria_data = [v['total'] for v in veiculos_secretaria]

    consumo_meses = models.Abastecimentos.objects.filter(data__gte=date.today()-timedelta(days=180)).values('data__month').annotate(
        total=Sum('quantidade'))
    consumo_meses_labels = [f"Mês {c['data__month']}" for c in consumo_meses]
    consumo_meses_data = [c['total'] for c in consumo_meses]

    # Tabelas
    ultimos_abastecimentos = models.Abastecimentos.objects.order_by('-data')[:5]
    cnh_vencendo = models.condutor.objects.filter(validadeCNH__lte=date.today() + timedelta(days=180))

    context = {
        'total_veiculos': total_veiculos,
        'total_condutores': total_condutores,
        'total_abastecimentos': total_abastecimentos,
        'veiculos_secretaria_labels': veiculos_secretaria_labels,
        'veiculos_secretaria_data': veiculos_secretaria_data,
        'consumo_meses_labels': consumo_meses_labels,
        'consumo_meses_data': consumo_meses_data,
        'ultimos_abastecimentos': ultimos_abastecimentos,
        'cnh_vencendo': cnh_vencendo,
    }

    return render (request,'dashcombustiveis.html',context)

#-------------- ABASTECIMENTOS -----------------------#
def abastecimentos(request):
    return render (request,'abastecimentos/abastecimentos.html',{})

def abastecimentos_list(request):
    # buscar = request.GET.get('buscar')
    # if buscar:
    #     abastecimentos = models.Abastecimentos.objects.filter(veiculo__placa__icontains = buscar)
    # else:
    abastecimentos = models.Abastecimentos.objects.all()
    return render(request, 'abastecimentos/abastecimentos_list.html', {'abastecimentos': abastecimentos})

def add_abastecimento(request):
    if request.method == "POST":
        form = forms.Abastecimentos_form(request.POST or None)
        print(form.is_valid())

        if form.is_valid():
            # print(form.cleaned_data)
            form.instance.valorTotal = form.instance.valorUnitario * form.instance.quantidade
            print(form.instance)
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "AbastecimentosListChanged": None,
                        "showMessage": f"Abastecimento registrado!"
                    })
                })
        else:
            return render(request, 'abastecimentos/abastecimentos_form.html', {
                'form': form,
            })
    else:
        form = forms.Abastecimentos_form()
    return render(request, 'abastecimentos/abastecimentos_form.html', {
        'form': form,
    })

def edit_abastecimento(request, abastecimento_pk):
    abastecimento_instance = models.Abastecimentos.objects.get(pk = abastecimento_pk)
    form = forms.Abastecimentos_form(request.POST or None, instance = abastecimento_instance)
    if request.POST:
        if form.is_valid:
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "AbastecimentosListChanged": None,
                        "showMessage": f"Abastecimento editado com sucesso!"
                    })
                })
        else:
            return render(request, 'abastecimentos/abastecimentos_form.html', {
                'form': form,
            })

    return render (request, 'abastecimentos/abastecimentos_form.html', {
        'form':form,
    })

#-------------- FROTA --------------------------------#
def frota(request):
    return render (request,'frota/frota.html',{})

def frota_list(request):
    frota = models.veiculo.objects.all()
    return render(request, 'frota/frota_list.html', {'frota': frota})

def add_frota(request):
    if request.method == "POST":
        form = forms.Frota_form(request.POST or None)
        print(form.is_valid())
        if form.is_valid():
            # ALTERAR A PARTIR DAQUI
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "FrotaListChanged": None,
                        "showMessage": f"Veículo registrado!"
                    })
                })
        else:
            return render(request, 'frota/frota_form.html', {
                'form': form,
            })
    else:
        form = forms.Frota_form()
    return render(request, 'frota/frota_form.html', {
        'form': form,
    })

def edit_frota(request, frota_pk):
    frota_instance = models.veiculo.objects.get(pk = frota_pk)
    form = forms.Frota_form(request.POST or None, instance = frota_instance)
    if request.POST:
        if form.is_valid:
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "FrotaListChanged": None,
                        "showMessage": f"Veículo editado com sucesso!"
                    })
                })
        else:
            return render(request, 'frota/frota_form.html', {
                'form': form,
            })

    return render (request, 'frota/frota_form.html', {
        'form':form,
    })

#-------------- CONDUTORES --------------------------------#
def condutores(request):
    return render (request,'condutores/condutores.html',{})

def condutores_list(request):
    condutores = models.condutor.objects.all()
    return render(request, 'condutores/condutores_list.html', {'condutores': condutores})

def add_condutores(request):
    if request.method == "POST":
        form = forms.Condutores_form(request.POST or None)
        if form.is_valid():
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "CondutoresListChanged": None,
                        "showMessage": f"Condutor registrado!"
                    })
                })
        else:
            return render(request, 'condutores/condutores_form.html', {
                'form': form,
            })
    else:
        form = forms.Condutores_form()
    return render(request, 'condutores/condutores_form.html', {
        'form': form,
    })

def edit_condutores(request, condutor_pk):
    condutores_instance = models.condutor.objects.get(pk = condutor_pk)
    form = forms.Condutores_form(request.POST or None, instance = condutores_instance)
    if request.POST:
        if form.is_valid:
            form.save()
            return HttpResponse(
                status=204,
                headers={
                    'HX-Trigger': json.dumps({
                        "CondutoresListChanged": None,
                        "showMessage": f"Condutor editado com sucesso!"
                    })
                })
        else:
            return render(request, 'condutores/condutores_form.html', {
                'form': form,
            })

    return render (request, 'condutores/condutores_form.html', {
        'form':form,
    })