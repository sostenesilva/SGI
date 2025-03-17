from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

# 🔹 Definição dos grupos e permissões
GRUPOS_PERMISSOES = {
    "Administrador do Sistema": ["add", "change", "delete", "view"],
    "Gestor de Configurações": ["add", "change", "delete", "view"],
    
    "Gestor de Contratos": ["add", "change", "delete", "view"],
    "Fiscal de Contrato": ["change", "view"],
    "Usuário Básico": ["view"],

    "Gestor de Frota": ["add", "change", "delete", "view"],
    "Analista de Abastecimento": ["add", "change", "view"],
    "Usuário Comum": ["view"],

    "Gestor de Protocolo": ["add", "change", "delete", "view"],
    "Analista de Protocolo": ["add", "change", "view"],
    "Recepcionista": ["add", "view"],
    
    "Gestor de Regularidade": ["add", "change", "delete", "view"],
    "Analista de Regularidade": ["add", "change", "view"],

    "Gestor da Transparência": ["add", "change", "delete", "view"],
    "Supervisor da Transparência": ["add", "change", "view"],
    "Usuário Responsável por Critérios": ["add", "view"],
}

# 🔹 Listar todos os models disponíveis nos aplicativos instalados
models_disponiveis = {
    model._meta.model_name: model
    for app_config in apps.get_app_configs()
    for model in app_config.get_models()
}

# 🔹 Criar/atualizar grupos e permissões
for grupo_nome, acoes in GRUPOS_PERMISSOES.items():
    grupo, created = Group.objects.get_or_create(name=grupo_nome)
    
    permissoes_para_adicionar = []
    
    for model_nome, model in models_disponiveis.items():
        content_type = ContentType.objects.get_for_model(model)

        for acao in acoes:
            codename = f"{acao}_{model_nome}"  # Exemplo: "add_contrato"
            perm = Permission.objects.filter(codename=codename, content_type=content_type).first()
            
            if perm:
                permissoes_para_adicionar.append(perm)
    
    grupo.permissions.set(permissoes_para_adicionar)  # Atualiza permissões do grupo
    print(f"📌 Grupo '{grupo_nome}' atualizado com {len(permissoes_para_adicionar)} permissões!")

print("✅ Todos os grupos e permissões foram criados/atualizados com sucesso!")
