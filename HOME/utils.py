from .models import Notificacao, Setor
from MGPROTOCOLO.models import Setor as SetorAntigo
from django.forms.models import model_to_dict


def notificar(usuario, titulo, mensagem):
    Notificacao.objects.create(usuario=usuario, titulo=titulo, mensagem=mensagem)

def migrar_setor():
    for setor in SetorAntigo.objects.all():
        data = model_to_dict(setor,exclude=['usuarios'])
        novo = Setor.objects.create(**data)
        novo.usuarios.set(setor.usuarios.all())