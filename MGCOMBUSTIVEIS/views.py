import base64
from collections import defaultdict
from datetime import date, datetime, timedelta
import json
from django.http import HttpResponse
from django.shortcuts import render
from weasyprint import HTML
from . import models, forms
from django.core.paginator import Paginator
from . import models
from django.db.models import Count, Sum
from django.template.loader import render_to_string
from django.db.models.functions import ExtractMonth

def dashcombustiveis(request):
    
    # Resumo geral
    total_veiculos = models.veiculo.objects.count()
    total_condutores = models.condutor.objects.count()
    total_abastecimentos = models.Abastecimentos.objects.count()

    # Gráficos
    veiculos_secretaria = models.veiculo.objects.values('secretaria__nome').annotate(total=Count('id'))
    veiculos_secretaria_labels = [v['secretaria__nome'] for v in veiculos_secretaria]  # Usando secretaria__nome
    veiculos_secretaria_data = [v['total'] for v in veiculos_secretaria]

    consumo_meses = models.Abastecimentos.objects.filter(
        data__gte=date.today() - timedelta(days=180)
    ).annotate(mes=ExtractMonth('data')).values('mes').annotate(total=Sum('quantidade'))

    consumo_meses_labels = [f"Mês {c['mes']}" for c in consumo_meses]
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

def emitir_relatorio(request):

    # Consultar opções para os filtros
    veiculos = models.veiculo.objects.all()
    condutores = models.condutor.objects.all()
    secretarias = models.veiculo.objects.values_list('secretaria', flat=True).distinct()

    if request.method == "POST":
        tipo_relatorio = request.POST.get("tipo_relatorio")

        # Obter a data atual para o cabeçalho
        agora = datetime.now()

        if tipo_relatorio == "abastecimento":
            # Filtros para abastecimentos
            veiculo_id = request.POST.get("veiculo")
            condutor_id = request.POST.get("condutor")
            periodo_inicio = request.POST.get("periodo_inicio")
            periodo_fim = request.POST.get("periodo_fim")
            status = request.POST.get("status")
            tipo_combustivel = request.POST.get("tipo_combustivel")

            abastecimentos = models.Abastecimentos.objects.all().order_by('veiculo', 'data')
            print('Abastecimentos:')
            print(abastecimentos)
        
            # Aplicar os filtros, se existirem
            if veiculo_id:
                abastecimentos = abastecimentos.filter(veiculo__id=veiculo_id)
            if condutor_id:
                abastecimentos = abastecimentos.filter(condutor__id=condutor_id)
            if periodo_inicio:
                abastecimentos = abastecimentos.filter(data__gte=periodo_inicio)
            if periodo_fim:
                abastecimentos = abastecimentos.filter(data__lte=periodo_fim)
            if status:
                abastecimentos = abastecimentos.filter(status=status)
            if tipo_combustivel:
                abastecimentos = abastecimentos.filter(tipo=tipo_combustivel)

            # Agrupar por veículo
            print('Abastecimentos agrupados (vazio):')

            abastecimentos_por_veiculo = defaultdict(list)
            print(abastecimentos_por_veiculo)
            for abastecimento in abastecimentos:
                abastecimentos_por_veiculo[abastecimento.veiculo].append(abastecimento)

            print('Abastecimentos agrupados:')
            print(abastecimentos_por_veiculo)

            print('Abastecimentos itens:')
            print(abastecimentos_por_veiculo.items())
            # Função para converter imagens estáticas em Base6
            with open("static/img/bg-timbrado-logo.png", "rb") as image_file:
                page_background = base64.b64encode(image_file.read()).decode('utf-8')

            # Renderizar o template do relatório de abastecimentos
            html_string = render_to_string(
                "relatorios/relatorio_abastecimentos.html", {"abastecimentos": abastecimentos_por_veiculo.items(), "agora": agora, 'page_background':page_background}
            )
            pdf_file = HTML(string=html_string).write_pdf()

            # Retornar o PDF
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = 'inline; filename="relatorio_abastecimentos.pdf"'
            return response

        elif tipo_relatorio == "condutor":
            # Filtros para condutores
            condutor_id = request.POST.get("condutor_id")
            secretaria = request.POST.get("secretaria")

            condutores = models.condutor.objects.all()

            # Aplicar os filtros, se existirem
            if condutor_id:
                condutores = condutores.filter(id=condutor_id)
            if secretaria:
                condutores = condutores.filter(nome__icontains=secretaria)

            # Renderizar o template do relatório de condutores
            html_string = render_to_string(
                "relatorios/relatorio_condutores.html", {"condutores": condutores, "agora": agora}
            )
            pdf_file = HTML(string=html_string).write_pdf()

            # Retornar o PDF
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = 'inline; filename="relatorio_condutores.pdf"'
            return response

        elif tipo_relatorio == "frota":
            # Filtros para frota
            veiculo_id = request.POST.get("veiculo_id")
            secretaria = request.POST.get("secretaria")

            veiculos = models.veiculo.objects.all()

            # Aplicar os filtros, se existirem
            if veiculo_id:
                veiculos = veiculos.filter(id=veiculo_id)
            if secretaria:
                veiculos = veiculos.filter(secretaria__icontains=secretaria)

            # Renderizar o template do relatório de frota
            html_string = render_to_string(
                "relatorios/relatorio_frota.html", {"veiculos": veiculos, "agora": agora}
            )
            pdf_file = HTML(string=html_string).write_pdf()

            # Retornar o PDF
            response = HttpResponse(pdf_file, content_type="application/pdf")
            response["Content-Disposition"] = 'inline; filename="relatorio_frota.pdf"'
            return response

        else:
            # Tipo de relatório não implementado
            return HttpResponse("Tipo de relatório não implementado.", status=400)

    # Retornar a página inicial com os filtros disponíveis
    context = {
        "veiculos": veiculos,
        "condutores": condutores,
        "secretarias": secretarias,
    }
    # Redirecionar para a página de seleção de relatórios, caso não seja POST
    return render(request, "relatorios/relatorios.html", context)