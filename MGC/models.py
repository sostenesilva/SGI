from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, User
import json
from django.db.models import Sum


class Fornecedores (models.Model):
    NumeroDocumentoAjustado = models.CharField(max_length=100, null=True, blank=True)
    RazaoSocial = models.CharField(max_length=200, null=True, blank=True)
    CPF_CNPJ = models.CharField(max_length=100, null=True, blank=True)
    Endereco = models.CharField(max_length=1000, null=True, blank=True)
    Representante = models.CharField(max_length=200, null=True, blank=True)
    Contato = models.CharField(max_length=100, null=True, blank=True)
    Email = models.EmailField(null=True, blank=True)
    Banco = models.CharField(max_length=200, null=True, blank=True)
    Agencia = models.CharField(max_length=200, null=True, blank=True)
    Conta = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return '{} - {}'.format(self.NumeroDocumentoAjustado,self.RazaoSocial)

class Contratos (models.Model):
    Fornecedor = models.ForeignKey(Fornecedores, on_delete=models.PROTECT)

    TipoProcesso = models.CharField(max_length=100, null=True, blank=True, verbose_name='Modalidade')
    LinkEdital = models.URLField(null=True, blank=True, verbose_name='Edital')
    LinkContrato = models.URLField(null=True, blank=True, verbose_name='Contrato')
    Situacao = models.CharField(max_length=50, null=True, blank=True)
    SiglaUG = models.CharField(max_length=10, null=True, blank=True, verbose_name='UG')
    Objeto = models.TextField(null=True, blank=True)
    Valor = models.FloatField(null=True, blank=True)
    UnidadeOrcamentaria = models.CharField(max_length=100, null=True, blank=True, verbose_name='Unidade Orçamentária')
    CodigoUG = models.CharField(max_length=10, null=True, blank=True)
    NumeroProcesso = models.CharField(max_length=10, null=True, blank=True, verbose_name='Processo')
    UnidadeGestora = models.CharField(max_length=100, null=True, blank=True, verbose_name='Unidade Gestora')
    CodigoContrato = models.CharField(max_length=10, null=True, blank=True)
    AnoContrato = models.CharField(max_length=4, null=True, blank=True, verbose_name='Ano')
    Vigencia = models.CharField(max_length=100, null=True, blank=True)
    Estagio = models.CharField(max_length=100, null=True, blank=True)
    CodigoPL = models.CharField(max_length=10, null=True, blank=True)
    NumeroDocumento = models.CharField(max_length=50, null=True, blank=True, verbose_name='Documento')
    Municipio = models.CharField(max_length=10, null=True, blank=True)
    TipoDocumento = models.CharField(max_length=10, null=True, blank=True)
    NumeroContrato = models.CharField(max_length=5, null=True, blank=True, verbose_name='Contrato')
    Esfera = models.CharField(max_length=1, null=True, blank=True)
    AnoProcesso = models.CharField(max_length=4, null=True, blank=True, verbose_name='Ano')

    AtualizarItens = models.BooleanField(default=True)
    AtualizarDados = models.BooleanField(default=True)

    def __str__(self) -> str:
        return '{}/{} - {} - {}'.format(self.NumeroContrato,self.AnoContrato,self.TipoProcesso,self.Fornecedor)

class TermoAditivo (models.Model):
    Contrato = models.ForeignKey(Contratos, on_delete=models.PROTECT)
    CodigoContrato = models.IntegerField(null=True, blank=True)
    LinkArquivo = models.URLField(null=True, blank=True)
    NumeroTermoAditivo = models.CharField(max_length=20, null=True, blank=True)
    Vigencia = models.CharField(max_length=200, null=True, blank=True)
    JustificativaTermoAditivo = models.TextField(null=True, blank=True)
    ValorTermoAditivo = models.FloatField(null=True,blank=True)
    AnoTermoAditivo = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f'Termo Aditivo {self.NumeroTermoAditivo}/{self.AnoTermoAditivo} - Contrato {self.Contrato}'

class Itens (models.Model):
    Contrato = models.ForeignKey(Contratos, on_delete=models.CASCADE)
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
    fiscal = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)

    totalEntradas = models.FloatField(null=True, blank=True, default=0)
    totalSaidas = models.FloatField(null=True, blank=True, default=0)
    saldoAtual = models.FloatField(null=True, blank=True, default=0)

    def __str__(self) -> str:
        return 'Contrato {} - {}'.format(self.contrato, self.sec)

class EntradaSec (models.Model):
    item = models.ForeignKey(Itens, on_delete=models.CASCADE)
    saldocontratosec = models.ForeignKey(SaldoContratoSec, on_delete=models.CASCADE, related_name='entradas')
    quantidade = models.IntegerField(null=True)
    dataehora = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return '{}'.format(self.item)
    
def diretorioOF (instance, filename):
    return 'ordem de fornecimento/{}'.format(filename)

class Ordem (models.Model):
    valor = models.FloatField(null=True, blank=True)
    arquivo = models.FileField(null=True, blank=True)
    dataehora = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    saldoContratosec = models.ForeignKey(SaldoContratoSec, on_delete=models.PROTECT, related_name='saidas')
    descricao = models.TextField(null=True, blank=True)
    codigo = models.UUIDField(null=True, blank=True)

    def __str__(self) -> str:
        return '{} - {} - {} - R$ {}'.format(self.codigo,self.saldoContratosec.contrato.Fornecedor.RazaoSocial, self.saldoContratosec.sec, self.valor)

class SaidaSec (models.Model):
    ordem = models.ForeignKey(Ordem, on_delete=models.CASCADE)
    item = models.ForeignKey(Itens, on_delete=models.CASCADE)
    quantidade = models.IntegerField(null=True)
    dataehora = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT)

    def __str__(self) -> str:
        return '{} - {}'.format(self.ordem.codigo, self.item)