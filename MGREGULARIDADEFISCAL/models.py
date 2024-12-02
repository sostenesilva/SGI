import uuid
from django.db import models
from MGC.models import Fornecedores
from django.contrib.auth.models import Group, User

def diretorioCertidao (instance, filename):
    return f'MGREGULARIDAFISCAL/certidões/{instance.dataEmissao.year}/{instance.tipo}/{instance.dataEmissao.day}-{instance.dataEmissao.month}-{instance.dataEmissao.year} - {instance.tipo} - {instance.fornecedor.RazaoSocial}.pdf'

class Certidao(models.Model):

    certidoes_choices = [
        ('FGTS','Certificado de Regularidade do FGTS - CRF'),
        ('FEDERAL','Certidão de Débitos Federais'),
        ('ESTADUAL','Certidão de Regularidade Fiscal Estadual'),
        ('CNDT','Certidão Negativa de Débitos Trabalhistas (CNDT)'),
        ('MUNICIPAL','Certidão de Regularidade Municipal'),
    ]

    fornecedor = models.ForeignKey(Fornecedores, on_delete=models.PROTECT, related_name = 'certidoes')
    tipo = models.CharField(max_length=15,choices=certidoes_choices)
    dataEmissao = models.DateField()
    dataValidade = models.DateField()
    autenticacao = models.CharField(max_length=100, null=True, blank=True)
    autor = models.ForeignKey(User, on_delete=models.PROTECT)
    arquivo = models.FileField(upload_to=diretorioCertidao)

    class Meta:
        unique_together = ('fornecedor', 'tipo', 'dataEmissao')  # Evita duplicidade

    def __str__(self):
        return f'{self.tipo} - {self.dataEmissao} à {self.dataValidade} - {self.fornecedor}'
    
class Declaracao(models.Model):
    fornecedor = models.ForeignKey(Fornecedores, on_delete=models.PROTECT)
    codigo = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    data_emissao = models.DateField(auto_now_add=True)

    def get_certidoes(self):
            """
            Retorna um dicionário com a certidão mais recente e válida de cada tipo.
            """
            certidoes = {}
            for tipo, _ in Certidao.certidoes_choices:
                certidao_valida = (
                    Certidao.objects.filter(fornecedor=self.fornecedor, tipo=tipo, dataValidade__gte = self.data_emissao)
                    .order_by('-dataEmissao')
                    .first()
                )
                certidoes[tipo] = certidao_valida
            return certidoes

    def __str__(self):
        return f'Declaração {self.codigo} - {self.fornecedor}'