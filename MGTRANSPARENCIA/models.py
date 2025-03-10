from django.db import models
from django.conf import settings
from HOME.models import Secretaria

class DbDimensao(models.Model):
    """Macrocategoria dos critérios."""
    dimensao = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.dimensao


class DbCriterios(models.Model):
    """Critérios de transparência exigidos pelo tribunal."""

    CLASSIFICACAO_CHOICES = [
        ('Obrigatória', 'Obrigatória'),
        ('Essencial', 'Essencial'),
        ('Recomendada', 'Recomendada'),
    ]

    PERIODICIDADE_CHOICES = [
        ('Diário', 'Diário'),
        ('Semanal', 'Semanal'),
        ('Quinzenal', 'Quinzenal'),
        ('Mensal', 'Mensal'),
        ('Bimestral', 'Bimestral'),
        ('Trimestral', 'Trimestral'),
        ('Quadrimestral', 'Quadrimestral'),
        ('Semestral', 'Semestral'),
        ('Anual', 'Anual'),
        ('Tempestivo', 'Tempestivo'),
    ]

    item = models.CharField(max_length=6, verbose_name="Código do Item")
    criterio = models.TextField(verbose_name="Descrição do Critério")
    dimensao = models.ForeignKey(DbDimensao, on_delete=models.PROTECT, blank=True, null=True, verbose_name="Dimensão")
    periodicidade = models.CharField(max_length=20, choices=PERIODICIDADE_CHOICES, null=True, blank=True, verbose_name="Periodicidade")
    classificacao = models.CharField(max_length=20, choices=CLASSIFICACAO_CHOICES, default='Obrigatório', verbose_name="Classificação")

    def __str__(self):
        return f'Item {self.item} - {self.criterio[:50]}... ({self.classificacao})'


class DbAvaliacao(models.Model):
    """Vinculação de um critério a uma secretaria responsável com prazo e periodicidade."""

    STATUS_CHOICES = [
        ('Atrasado', 'Atrasado'),
        ('Em dia', 'Em dia'),
        ('pendência', 'Com pendência'),
    ]

    criterio = models.ForeignKey(DbCriterios, on_delete=models.PROTECT, verbose_name="Critério Avaliado")
    responsavel = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.PROTECT, verbose_name="Responsável")
    secretaria = models.ForeignKey(Secretaria, null=True, on_delete=models.PROTECT, verbose_name="Secretaria")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Em dia', verbose_name="Status")

    def __str__(self):
        return f'{self.criterio.item} - ({self.secretaria} - {self.responsavel})'

def diretorio_item_avaliacao(instance, filename):
    """Define o diretório de upload para arquivos de avaliação."""
    return f'MGTRANSPARENCIA/criterios/{instance.avaliacao.criterio.item}/{instance.avaliacao.secretaria}/{instance.id} - {filename}'

class DbAvaliacaoLog(models.Model):
    """Histórico de envios de documentos e sua avaliação."""

    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Atrasado', 'Atrasado'),
        ('Em análise', 'Em análise'),
        ('Publicado', 'Publicado'),
        ('Publicado com atraso', 'Publicado com atraso'),
    ]

    avaliacao = models.ForeignKey(DbAvaliacao, on_delete=models.CASCADE, related_name="logs", verbose_name="Avaliação")
    arquivo = models.FileField(null=True, blank=True, upload_to=diretorio_item_avaliacao, verbose_name="Anexo", max_length=300)
    anotacao = models.TextField(null=True, blank=True, verbose_name="Anotação")
    data_envio = models.DateTimeField(null=True, blank=True, verbose_name="Data de Envio")
    data_limite = models.DateTimeField(null=True, blank=True, verbose_name="Data Limite")
    data_publicacao = models.DateTimeField(null=True, blank=True, verbose_name="Data de Publicação")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pendente', verbose_name="Status")
    enviado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="Enviado_por")
    publicado_por = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="Publicado_por")

    def save(self, *args, **kwargs):
        """Atualiza automaticamente o status conforme a presença do arquivo."""
        if self.arquivo and self.status == 'Pendente':
            self.status = 'Em análise'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Tarefa {self.id} - {self.avaliacao} - {self.data_limite}'
    

def diretorio_manual_criterio(instance, filename):
    """Define o diretório de upload para manuais dos critérios."""
    return f'MGTRANSPARENCIA/manuais/{filename}'

class InformacoesCriterio (models.Model):
    CATEGORIA_CHOICES = [
    ('link', 'Links Úteis'),
    ('documento', 'Documento'),
    ('anotacao', 'Anotação'),
    ]

    STATUS_CHOICES = [
    ('atual', 'Atual'),
    ('desatualizado', 'Desatualizado'),
    ]

    criterio = models.ForeignKey(DbCriterios, on_delete=models.SET_NULL, null=True, blank=True)
    categoria = models.CharField(max_length=25, choices=CATEGORIA_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    anotacao = models.TextField(null=True, blank=True)
    documento = models.FileField(upload_to= diretorio_manual_criterio, null=True, blank=True)
    geral = models.BooleanField(default=False)

    def __str__(self):
        return f'Log {self.categoria} - {self.anotacao[:50]}...'
