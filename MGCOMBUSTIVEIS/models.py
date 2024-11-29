from django.db import models
from django.contrib.auth.models import Group, User

class veiculo (models.Model):
    placa = models.CharField(max_length=8)
    secretaria = models.CharField(max_length=50)
    modelo = models.CharField(max_length=100, null=True)
    descricao = models.TextField(null=True)
    observacao = models.TextField(null=True)

    def __str__(self):
        return f'{self.placa} - {self.modelo} - {self.secretaria}'

class fiscal (models.Model):
    nome = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.nome.username}'

class condutor (models.Model):
    nome = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.nome.username}'

class Abastecimentos (models.Model):
    data = models.DateField()
    veiculo = models.ForeignKey(veiculo, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=30)
    quantidade = models.FloatField()
    valorUnitario = models.FloatField()
    valorTotal = models.FloatField()
    condutor = models.ForeignKey(condutor, on_delete=models.PROTECT)
    fiscal = models.ForeignKey(fiscal, on_delete=models.PROTECT)
    km = models.IntegerField()
    status = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.veiculo.placa} - {self.data} - {self.tipo} - R${self.valorTotal}'
