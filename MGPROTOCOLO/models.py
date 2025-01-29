from django.db import models
from django.contrib.auth.models import User


class Setor(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome

def diretorioDocumento (instance, filename):
    return f'MGPROTOCOLO/documentos/{instance.data_criacao.year}/{instance.origem}/{instance.id} - {filename}'


class Documento(models.Model):
    TIPO_CHOICES = [
        ('Memorando', 'Memorando'),
        ('Ofício', 'Ofício'),
        ('Relatório', 'Relatório'),
        ('Outro', 'Outro'),
    ]
    STATUS_CHOICES = [
        ('Criado', 'Criado'),
        ('Em Tramitação', 'Em Tramitação'),
        ('Concluído', 'Concluído'),
    ]

    titulo = models.CharField(max_length=200)
    arquivo = models.FileField(upload_to=diretorioDocumento, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    descricao = models.TextField(null=True, blank=True)
    origem = models.ForeignKey(Setor, related_name='documentos_criados', on_delete=models.PROTECT, null=True, blank=True)
    destino = models.ForeignKey(Setor, related_name='documentos_recebidos', on_delete=models.PROTECT, null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.PROTECT)
    data_criacao = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    data_conclusao = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Criado')

    def __str__(self):
        return f"{self.tipo} - {self.titulo}"


class Movimentacao(models.Model):
    documento = models.ForeignKey(Documento, related_name='movimentacoes', on_delete=models.CASCADE, null=True, blank=True)
    origem = models.ForeignKey(Setor, related_name='movimentacoes_enviadas', on_delete=models.PROTECT, null=True, blank=True)
    destino = models.ForeignKey(Setor, related_name='movimentacoes_recebidas', on_delete=models.PROTECT, null=True, blank=True)
    data_movimentacao = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    observacao = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Movimentação de {self.origem} para {self.destino}"

def diretorioProtocolo (instance, filename):
    return f'MGPROTOCOLO/protocolos/{instance.data_criacao.year}/{instance.destino}/{instance.numero} - {filename}'

class ProtocoloMovimentacao(models.Model):
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Finalizado', 'Finalizado'),
    ]

    numero = models.CharField(max_length=20, unique=True)  # Ex.: PM-0001/2025
    data_criacao = models.DateTimeField(auto_now_add=True)
    destino = models.ForeignKey(Setor, on_delete=models.PROTECT, related_name="protocolos_recebidos")
    arquivo_assinado = models.FileField(upload_to=diretorioProtocolo, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pendente")
    movimentacoes = models.ManyToManyField(Movimentacao, related_name="protocolos")

    def __str__(self):
        return f"{self.numero} - {self.destino.nome}"
