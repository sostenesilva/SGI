from django.shortcuts import render, get_object_or_404
from .models import Modulo, Notificacao
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import Group, Permission, User
from django.template.loader import render_to_string

@login_required
def novoportal(request):
    return render(request, 'base2.html', {})


@login_required
def portal_inicial(request):
    modulos = Modulo.objects.all()
    return render(request, 'portal_inicial.html', {'modulos': modulos})

login_required
def modulo_detalhes(request, modulo_id):
    modulo = get_object_or_404(Modulo, pk=modulo_id)
    return render(request, 'modulo_detalhes.html', {'modulo': modulo})


def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'listar_usuarios.html',{'usuarios':usuarios})

def privilegios(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    permissoes = Permission.objects.all()
    grupos = Group.objects.all()
    return render(request, "privilegios.html", {"grupos": grupos, 'user':usuario})

def carregar_permissoes(request, user_id, grupo_id):
    usuario = get_object_or_404(User, id=user_id)
    grupo = get_object_or_404(Group, id=grupo_id)
    permissoes = grupo.permissions.all()
    permissoes_usuario = usuario.user_permissions.values_list("id", flat=True)  # Obtém IDs das permissões do usuário

    return render(request, "permissoes_lista.html", {"permissoes": permissoes, "grupo": grupo, 'user':usuario, "permissoes_usuario": list(permissoes_usuario)})

def atualizar_permissao_usuario(request, user_id, grupo_id, permissao_id):
    usuario = get_object_or_404(User, id=user_id)
    permissao = get_object_or_404(Permission, id=permissao_id)

    permissoes_usuario = list(usuario.user_permissions.values_list("id", flat=True))  # Obtém IDs das permissões do usuário
    if permissao.id in permissoes_usuario:
        usuario.user_permissions.remove(permissao)
        status = "removida"
    else:
        usuario.user_permissions.add(permissao)
        status = "adicionada"

    return JsonResponse({"status": status, "permissao": permissao.codename})


def listar_notificacoes(request, user_id):
    usuario = User.objects.get(pk = user_id)
    notificacoes = Notificacao.objects.filter(usuario=usuario)

    return render(request, 'listar_notificacoes.html',{'notificacoes':notificacoes})

@login_required
def notificacoes_quantidade(request):
    notificacoes_nao_lidas = Notificacao.objects.filter(usuario=request.user, lida=False)
    html = render_to_string("notificacao_badge.html", {
        "notificacoes_nao_lidas": notificacoes_nao_lidas
    })
    return HttpResponse(html)


@login_required
def notificacoes_conteudo(request):
    notificacoes = Notificacao.objects.filter(usuario=request.user).order_by('-criada_em')[:5]
    return render(request, "notificacoes.html", {
        "notificacoes": notificacoes
    })



########### AJUSTAR GRUPOS E PERMISSÕES #####################
def grupos_permissoes(request):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from django.apps import apps

    # 🔹 Dicionário com os módulos, suas funções e permissões
    MGC = {
        'Acessar':['autorizado'],
        'Contrato': ['adicionar', 'editar', 'deletar'],
        'Fornecedor': ['adicionar', 'editar', 'deletar'],
        'Saldos': ['adicionar', 'editar', 'deletar'],
        'Ordem': ['adicionar', 'editar', 'deletar'],
        'Pagamento': ['adicionar', 'editar', 'deletar'],
    }
    MGREGULARIDADE = {
        'Acessar':['autorizado'],
        'Fornecedor': ['adicionar', 'editar', 'deletar'],
        'Certidao': ['adicionar', 'editar', 'deletar'],
        'Declaracao': ['adicionar', 'editar', 'deletar'],
    }
    MGCOMBUSTIVEIS = {
        'Acessar':['autorizado'],
        'Abastecimento': ['adicionar', 'editar', 'deletar'],
        'Frota': ['adicionar', 'editar', 'deletar'],
        'Condutor': ['adicionar', 'editar', 'deletar'],
        'Relatorio': ['emitir'],
    }
    MGTRANSPARENCIA = {
        'Acessar':['autorizado'],
        'Criterios': ['adicionar', 'editar', 'deletar'],
        'Avaliacao': ['adicionar', 'editar', 'deletar'],
        'Tarefa': ['adicionar', 'editar', 'deletar'],
        'Envio': ['adicionar'],
    }
    MGPROTOCOLO = {
        'Acessar':['autorizado'],
        'Processo': ['adicionar', 'editar', 'deletar'],
        'Movimentacao': ['adicionar', 'editar', 'deletar'],
        'ProtocoloManual': ['adicionar', 'editar', 'deletar'],
    }

    # 🔹 Lista organizada de módulos
    modulos = {
        "MGC": MGC,
        "MGCOMBUSTIVEIS": MGCOMBUSTIVEIS,
        "MGPROTOCOLO": MGPROTOCOLO,
        "MGREGULARIDADE": MGREGULARIDADE,
        "MGTRANSPARENCIA": MGTRANSPARENCIA,
    }

    # 🔹 Criar grupos e atribuir permissões
    for nome_modulo, funcoes in modulos.items():
        try:
            nome_grupo = f"{nome_modulo}"
            grupo, _ = Group.objects.get_or_create(name=nome_grupo)

            for funcao, permissoes in funcoes.items():
                for permissao in permissoes:
                    codename = f"{permissao}_{funcao}_{nome_modulo}"
                    nome_permissao = f"Pode {permissao} {funcao} no módulo {nome_modulo}"
                    content_type = ContentType.objects.get_for_model(Permission)

                    # 🔹 Criar ou atualizar a permissão
                    perm, created = Permission.objects.get_or_create(
                        codename=codename,
                        name=nome_permissao,
                        content_type=content_type,
                    )

                    grupo.permissions.add(perm)

            grupo.save()
            print(f"✅ Grupo '{nome_grupo}' atualizado com sucesso!")

        except Exception as e:
            print(f"❌ Erro ao processar o módulo {nome_modulo}: {e}")

    print("🎯 Grupos e permissões criados/atualizados com sucesso!")

