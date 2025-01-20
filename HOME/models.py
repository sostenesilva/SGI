from django.db import models

class Modulo(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    link_modulo = models.CharField(max_length=100)  # Link para acessar o módulo principal

    def __str__(self):
        return self.nome

class Tutorial(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    link_arquivo = models.URLField(blank=True, null=True)  # Link para PDF ou outro material
    modulo = models.ForeignKey(Modulo, related_name="tutoriais", on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo
