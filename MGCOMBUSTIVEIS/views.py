import json
from django.http import HttpResponse
from django.shortcuts import render
from . import models, forms
from django.core.paginator import Paginator



def dashcombustiveis(request):
    
    context = {
    }

    return render (request,'dashcombustiveis.html',context)


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
