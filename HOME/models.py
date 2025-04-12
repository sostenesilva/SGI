from django.db import models
from django.contrib.auth.models import User, Permission


class Secretaria(models.Model):
    nome = models.CharField(max_length=255, unique=True, null=True, blank=True)
    sigla = models.CharField(max_length=10, blank=True, null=True)
    usuarios = models.ManyToManyField(User, related_name='secretaria_home', null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Setor(models.Model):
    nome = models.CharField(max_length=255, unique=True, null=True, blank=True)
    secretaria = models.ForeignKey(Secretaria, on_delete=models.SET_NULL, null=True, blank=True)
    usuarios = models.ManyToManyField(User, null=True, blank=True)
    sigla = models.CharField(max_length=10, blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Modulo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    link_modulo = models.CharField(max_length=100)  # Link para acessar o módulo principal
    sigla = models.CharField(max_length=100, null=True, blank=True)
    permissao = models.ForeignKey(Permission, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome

def diretorioTutorial (instance, filename):
    return f'HOME/Tutoriais/{instance.modulo}/{instance.titulo}.pdf'

class Tutorial(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    arquivo = models.FileField(upload_to=diretorioTutorial,blank=True, null=True)  # Link para PDF ou outro material
    modulo = models.ForeignKey(Modulo, related_name="tutoriais", on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

class Notificacao(models.Model):
    titulo = models.CharField(max_length=255)
    mensagem = models.TextField()
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    lida = models.BooleanField(default=False)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.titulo} para {self.usuario.username}'