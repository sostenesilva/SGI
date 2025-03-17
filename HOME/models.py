from django.db import models
from django.contrib.auth.models import User


class Secretaria(models.Model):
    nome = models.CharField(max_length=255, unique=True, null=True, blank=True)
    sigla = models.CharField(max_length=10, blank=True, null=True)
    usuarios = models.ManyToManyField(User, related_name='secretaria_home', null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Modulo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    link_modulo = models.CharField(max_length=100)  # Link para acessar o módulo principal
    sigla = models.CharField(max_length=100, null=True, blank=True)

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
