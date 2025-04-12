from .models import Notificacao, Setor
# from MGPROTOCOLO.models import Setor as SetorAntigo
from django.forms.models import model_to_dict
from MGPROTOCOLO import models as modelsMGPROTOCOLO


def notificar(usuario, titulo, mensagem):
    Notificacao.objects.create(usuario=usuario, titulo=titulo, mensagem=mensagem)

# def migrar_setor():
#     for setor in SetorAntigo.objects.all():
#         data = model_to_dict(setor,exclude=['usuarios'])
#         novo = Setor.objects.create(**data)
#         novo.usuarios.set(setor.usuarios.all())

def migrar_protocolos():
    processos = modelsMGPROTOCOLO.Processo.objects.all()
    movi = modelsMGPROTOCOLO.Movimentacao.objects.all()
    protmovi = modelsMGPROTOCOLO.ProtocoloMovimentacao.objects.all()
    setornovo = Setor.objects.all()

    for item in processos:
        if item.setor_demandante:
            item.demandante = setornovo.get(nome = item.setor_demandante.nome)
        if item.setor_fim:
            item.fim = setornovo.get(nome = item.setor_fim.nome)
        if item.setor_atual:
            item.atual = setornovo.get(nome = item.setor_atual.nome)
        item.save()

    for item in movi:
        if item.setor_origem:
            item.remetente = setornovo.get(nome = item.setor_origem.nome)
        if item.setor_destino:
            item.destinario = setornovo.get(nome = item.setor_destino.nome)
        item.save()


    for item in protmovi:
        if item.setor_destino:
            item.destinatario = setornovo.get(nome = item.setor_destino.nome)
        item.save()

        