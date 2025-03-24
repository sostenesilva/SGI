from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group, User
import json
from django.db.models import Sum
from HOME.models import Secretaria

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
    ug_choice = [
        ('PMC','Prefeitura'),
        ('FMS','Saúde'),
        ('FMAS','Assistência'),
        ('FMEC','Educação'),
        ('CORTESPREV','CortêsPREV'),
    ]

    estagio_choice = [
        ('Execução','Em Execução'),
        ('Suspenso','Suspenso'),
        ('Fim da Vigência','Concluído - Fim da Vigência'),
        ('Anulado','Concluído - Anulado'),
        ('Rescindido','Concluído - Rescindido'),        
    ]

    Fornecedor = models.ForeignKey(Fornecedores, on_delete=models.PROTECT)
    Objeto = models.TextField(null=True, blank=True)

    NumeroProcesso = models.CharField(max_length=10, null=True, blank=True, verbose_name='Processo')
    AnoProcesso = models.CharField(max_length=4, null=True, blank=True, verbose_name='Ano')
    TipoProcesso = models.CharField(max_length=100, null=True, blank=True, verbose_name='Modalidade')

    NumeroContrato = models.CharField(max_length=5, null=True, blank=True, verbose_name='Contrato')
    AnoContrato = models.CharField(max_length=4, null=True, blank=True, verbose_name='Ano')
    Estagio = models.CharField(max_length=100, choices=estagio_choice, null=True, blank=True)

    LinkContrato = models.URLField(null=True, blank=True, verbose_name='Contrato')
    LinkEdital = models.URLField(null=True, blank=True, verbose_name='Edital')
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)

    UnidadeGestora = models.CharField(max_length=100, choices=ug_choice, null=True, blank=True, verbose_name='Unidade Gestora')
    Valor = models.FloatField(null=True, blank=True)

    AtualizarItens = models.BooleanField(default=True)
    AtualizarDados = models.BooleanField(default=True)

    def __str__(self) -> str:
        return '{}/{} - {} - {}'.format(self.NumeroContrato,self.AnoContrato,self.TipoProcesso,self.Fornecedor)

class TermoAditivoValor (models.Model):
    Contrato = models.ForeignKey(Contratos, on_delete=models.PROTECT)

    NumeroTermoAditivo = models.CharField(max_length=20, null=True, blank=True)
    AnoTermoAditivo = models.IntegerField(null=True, blank=True)
    ValorTermoAditivo = models.FloatField(null=True,blank=True)
    LinkArquivo = models.URLField(null=True, blank=True)
    JustificativaTermoAditivo = models.TextField(null=True, blank=True)
    data_inicio = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self) -> str:
        return f'Termo Aditivo de Valor {self.NumeroTermoAditivo}/{self.AnoTermoAditivo} - Contrato {self.Contrato}'

class Itens (models.Model):
    Contrato = models.ForeignKey(Contratos, on_delete=models.CASCADE)
    Descricao = models.TextField(null=True, blank=True)
    Unidade = models.CharField(max_length=50, null=True, blank=True)
    PrecoUnitario = models.FloatField(null=True, blank=True)
    Quantidade = models.IntegerField(null=True, blank=True)
    Quantidade_disp = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return '{}'.format(self.Descricao)

class SaldoContratoSec(models.Model):
    contrato = models.ForeignKey(Contratos, on_delete=models.PROTECT)
    sec = models.ForeignKey(Secretaria, on_delete= models.PROTECT, verbose_name='Secretaria')
    fiscal = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)

    totalEntradas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
    totalSaidas = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)
    saldoAtual = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, default=0)

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