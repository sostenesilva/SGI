from django.db import models
from django.contrib.auth.models import Group, User
from HOME.models import Secretaria

class veiculo(models.Model):

    placa = models.CharField(max_length=8)
    ano = models.IntegerField(null=True, blank=True)
    modelo = models.CharField(max_length=100, null=True, blank=True)
    secretaria = models.ForeignKey(Secretaria, on_delete=models.PROTECT)
    descricao = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=60, choices=[('Em atividade','Em atividade'),('Em manutenção','Em manutenção'),('Excluído da frota','Excluído da frota')])
    observacao = models.TextField(null=True, blank=True)
    propriedade = models.CharField(max_length=60, choices=[('Próprio','Próprio'),('Contratado','Contratado')])

    def __str__(self):
        return f'{self.placa} - {self.modelo} - {self.secretaria}'

class fiscal (models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return f'{self.nome}'

class condutor (models.Model):
    nome = models.CharField(max_length=100)
    cpf = models.CharField(max_length=30, null=True, blank=True)
    datanascimento = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=30, choices=[('Ativo','Ativo'),('Desligado','Desligado')], default='Ativo')
    validadeCNH = models.DateField(null=True,blank=True)
    categoriaCNH = models.CharField(max_length=2, null=True, blank=True)
    cursoEscolar = models.BooleanField(default=False)
    observacoes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.nome}'

class Abastecimentos (models.Model):

    tipo_combustiveis = [
        ('Gasolina','Gasolina'),
        ('Diesel Comum','Diesel Comum'),
        ('Diesel S-10','Diesel S-10'),
        ('GNV','GNV'),
        ('Etanol','Etanol'),
    ]

    status_choice = [
        ('Aprovado','Aprovado'),
        ('Pendente','Pendente'),
        ('Negado','Negado'),
    ]
    data = models.DateField(null=True)
    veiculo = models.ForeignKey(veiculo, on_delete=models.PROTECT)
    tipo = models.CharField(max_length=30,choices=tipo_combustiveis)
    quantidade = models.FloatField(null=True)
    valorUnitario = models.FloatField(null=True)
    valorTotal = models.FloatField(null=True)
    condutor = models.ForeignKey(condutor, on_delete=models.PROTECT)
    fiscal = models.ForeignKey(fiscal, on_delete=models.PROTECT)
    km = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=10,choices=status_choice,default='Pendente')

    def __str__(self):
        return f'{self.veiculo.placa} - {self.data} - {self.tipo} - R${self.valorTotal}'
