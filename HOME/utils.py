from .models import Notificacao

def notificar(usuario, titulo, mensagem):
    Notificacao.objects.create(usuario=usuario, titulo=titulo, mensagem=mensagem)