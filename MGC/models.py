from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, User
import json

class Contratos (models.Model):
    TipoProcesso = models.CharField(max_length=100, null=True, blank=True)
    NumeroDocumentoAjustado = models.CharField(max_length=100, null=True, blank=True)
    RazaoSocial = models.CharField(max_length=200, null=True, blank=True)
    CPF_CNPJ = models.CharField(max_length=100, null=True, blank=True)
    LinkEdital = models.URLField(null=True, blank=True)
    LinkContrato = models.URLField(null=True, blank=True)
    Situacao = models.CharField(max_length=50, null=True, blank=True)
    SiglaUG = models.CharField(max_length=10, null=True, blank=True)
    Objeto = models.TextField(null=True, blank=True)
    Valor = models.FloatField(null=True, blank=True)
    UnidadeOrcamentaria = models.CharField(max_length=100, null=True, blank=True)
    CodigoUG = models.CharField(max_length=10, null=True, blank=True)
    PortariaComissaoLicitacao = models.CharField(max_length=100, null=True, blank=True)
    NumeroProcesso = models.CharField(max_length=10, null=True, blank=True)
    UnidadeGestora = models.CharField(max_length=100, null=True, blank=True)
    CodigoContrato = models.CharField(max_length=10, null=True, blank=True)
    AnoContrato = models.CharField(max_length=4, null=True, blank=True)
    Vigencia = models.CharField(max_length=100, null=True, blank=True)
    Estagio = models.CharField(max_length=100, null=True, blank=True)
    CodigoPL = models.CharField(max_length=10, null=True, blank=True)
    NumeroDocumento = models.CharField(max_length=50, null=True, blank=True)
    Municipio = models.CharField(max_length=10, null=True, blank=True)
    TipoDocumento = models.CharField(max_length=10, null=True, blank=True)
    NumeroContrato = models.CharField(max_length=5, null=True, blank=True)
    Esfera = models.CharField(max_length=1, null=True, blank=True)
    AnoProcesso = models.CharField(max_length=4, null=True, blank=True)
    
    def __str__(self) -> str:
        return '{}/{} - {}'.format(self.NumeroContrato,self.AnoContrato,self.TipoProcesso)

def diretorioOF (instance, filename):
    return 'ordem de fornecimento/{}'.format(filename)

class Itens (models.Model):
    Descricao = models.TextField(null=True, blank=True)
    CodigoContratoOriginal = models.CharField(max_length=10)
    Unidade = models.CharField(max_length=50, null=True, blank=True)
    PrecoUnitario = models.FloatField(null=True, blank=True)
    CodigoItem = models.CharField(max_length=10, null=True, blank=True)
    Quantidade = models.IntegerField(null=True, blank=True)
    PrecoTotal = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return '{}'.format(self.Descricao)


class SaldoContratoSec(models.Model):
    contrato = models.ForeignKey(Contratos, on_delete=models.PROTECT)
    sec = models.ForeignKey(Group, on_delete= models.PROTECT, verbose_name='Secretaria')
    saldo = models.FloatField(null=True, blank=True, default=0)
    fiscal = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return 'Contrato {} - {}'.format(self.contrato, self.sec)

class EntradaSec (models.Model):
    contrato = models.ForeignKey(Contratos, on_delete=models.PROTECT)
    sec = models.ForeignKey(Group, on_delete= models.PROTECT, verbose_name='Secretaria')
    item = models.ForeignKey(Itens, on_delete=models.CASCADE)
    saldocontratosec = models.ForeignKey(SaldoContratoSec, on_delete=models.CASCADE)
    quantidade = models.IntegerField(null=True)
    dataehora = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return '{}'.format(self.item)

class Ordem (models.Model):
    valor = models.FloatField(null=True, blank=True)
    arquivo = models.FileField(null=True, blank=True, upload_to= diretorioOF)
    dataehora = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)
    SaldoContratoSec = models.ForeignKey(SaldoContratoSec, on_delete=models.PROTECT)
    descricao = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return 'Contrato {} - {} - R$ {}'.format(self.SaldoContratoSec.contrato, self.SaldoContratoSec.sec, self.valor)

class SaidaSec (models.Model):
    ordem = models.ForeignKey(Ordem, on_delete=models.CASCADE)
    contrato = models.ForeignKey(Contratos, on_delete=models.CASCADE)
    item = models.ForeignKey(Itens, on_delete=models.CASCADE)
    quantidade = models.IntegerField(null=True)
    dataehora = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)
    totalporitem = models.FloatField(null=True, blank=True)

    def __str__(self) -> str:
        return '{} - {} - R$ {}'.format(self.ordem, self.contrato, self.item)