from datetime import date
import os
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from HOME.models import Setor as SetorHome
from HOME.models import Secretaria as SecretariaHome

def diretorioDocumento (instance, filename):
    extensao = os.path.splitext(filename)[1]
    filename = filename.replace("/","-")[:10]
    filename = '{}.{}'.format(filename,extensao)
    return f'MGPROTOCOLO/documentos/{instance.processo.criado_em.year}/{instance.processo.demandante.nome}/{filename}'

def diretorioProtocolo (instance, filename):
    extensao = os.path.splitext(filename)[1]
    return f'MGPROTOCOLO/protocolos/{instance.criado_em.year}/{instance.destinatario.nome}/{instance.criado_em} por {instance.criado_por.username} - id {instance.id}{extensao}'

class Processo(models.Model):
    STATUS_CHOICES = [
        ('em_analise', 'Em análise'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
        ('arquivado', 'Arquivado'),
    ]

    MODALIDADE_CHOICES = [
        ('digital', 'Digital'),
        ('fisico', 'Físico'),
    ]

    numero = models.CharField(max_length=100, unique=True, db_index=True, null=True, blank=True)
    titulo = models.CharField(max_length=255, null=True, blank=True)
    descricao = models.TextField(blank=True, null=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    demandante = models.ForeignKey(SetorHome, on_delete=models.SET_NULL, null=True, blank=True, related_name='SetorDemandante')
    fim = models.ForeignKey(SetorHome, on_delete=models.SET_NULL, null=True, blank=True, related_name='SetorFim')
    atual = models.ForeignKey(SetorHome, on_delete=models.SET_NULL, null=True, blank=True, related_name='SetorAtual')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_analise', null=True, blank=True)
    prazo = models.DateField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True, null=True, blank=True)
    ultima_movimentacao = models.ForeignKey('Movimentacao', on_delete=models.SET_NULL, null=True, blank=True, related_name='processo_ultima_movimentacao')
    ativo = models.BooleanField(default=True)
    modalidade = models.CharField(max_length=15,choices=MODALIDADE_CHOICES, default='fisico')
    
    def __str__(self):
        return f"{self.numero} - {self.titulo}"

    def clean(self):
        if self.demandante == self.fim:
            raise ValidationError("O setor demandante não pode ser o mesmo que o setor responsável.")
        
    def validate_unique(self, exclude=None):
        super().validate_unique(exclude)
        # Verifica se já existe outro processo com o mesmo número
        if Processo.objects.filter(numero=self.numero).exclude(pk=self.pk).exists():
            raise ValidationError({'numero': "Já existe um processo com esse número."})

    def esta_ativo(self):
        """
        Retorna True se o processo estiver ativo, False caso contrário.
        """
        return self.ativo

    def tempo_restante(self):
        """
        Retorna o número de dias restantes para o prazo do processo.
        Se o prazo já passou, retorna None.
        """
        if self.prazo:
            dias_restantes = (self.prazo - date.today()).days
            return max(dias_restantes, 0) if dias_restantes > 0 else None
        return None
    
    def resumo_movimentacoes(self):
        """
        Retorna um resumo das movimentações do processo.
        """
        resumo = []
        for movimentacao in self.movimentacoes.all():
            resumo.append({
                'data': movimentacao.realizado_em.strftime('%d/%m/%Y %H:%M'),
                'remetente': movimentacao.remetente.nome,
                'destinatario': movimentacao.destinatario.nome,
                'status': movimentacao.get_status_display(),
            })
        return resumo
    
    def esta_em_atraso(self):
        """
        Retorna True se o prazo do processo já passou, False caso contrário.
        """
        if self.prazo:
            return date.today() > self.prazo
        return False

    def total_documentos(self):
        """
        Retorna o número total de documentos associados ao processo.
        """
        return self.documentos.count()
    
    def setores_envolvidos(self):
        """
        Retorna uma lista de todos os setores envolvidos no processo.
        """
        setores = set()
        for movimentacao in self.movimentacoes.all():
            setores.add(movimentacao.remetente.nome)
            if self.atual!= None:
                setores.add(movimentacao.destinatario.nome)
            else:
                setores.add('Arquivo')
        return list(setores)

    @classmethod
    def processos_no_setor(cls, setor):
        """
        Retorna os processos cuja última movimentação está no setor especificado.
        """
        return cls.objects.filter(atual__in=setor).order_by('-atualizado_em')

    @classmethod
    def processos_encaminhados_pelo_setor(cls, setor):
        """
        Retorna os processos que foram encaminhados pelo setor especificado para outros setores.
        """
        return cls.objects.filter(movimentacoes__remetente__in=setor).distinct()
    
    def usuario_pode_modificar(self, usuario):
        """
        Verifica se o usuário pertence ao setor atual do processo.
        """
        return usuario in self.atual.usuarios.all() if self.atual else False
    
    def arquivar(self):
        """ Define o processo como arquivado """
        self.status = 'arquivado'
        self.atual = None  # Remove o setor atual, pois foi arquivado
        self.save()

class Documento(models.Model):
    TIPO_CHOICES = [
        ('inicial', 'Documento Inicial'),
        ('complementar', 'Documento Complementar'),
    ]

    CLASSIFICACAO_CHOICES = [
        ('oficio', 'Ofício'),
        ('ci', 'Comunicado Interno'),
        ('despacho', 'Despacho'),
        ('memorando', 'Memorando'),
        ('parecer', 'Parecer'),
        ('laudo', 'Láudo'),
        ('relatorio', 'Relatório'),
        ('contrato', 'Contrato'),
        ('edital', 'Edital'),
        ('cotacoes', 'Cotações'),
        ('outros', 'Outros'),
    ]

    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='documentos', null=True, blank=True)
    descricao = models.CharField(max_length=255, null=True, blank=True)
    classificacao = models.CharField(max_length=100, choices=CLASSIFICACAO_CHOICES, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='inicial', null=True, blank=True)
    arquivo = models.FileField(upload_to=diretorioDocumento, null=True, blank=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    criado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.descricao

class Movimentacao(models.Model):
    STATUS_CHOICES = [
        ('em_tramitacao', 'Em tramitação'),
        ('recebida', 'Recebida'),
        ('arquivada', 'Arquivada')
    ]

    RECEBIMENTO_CHOICES = [
        ('pendente', 'Pendente'),
        ('manual', 'Manual'),
        ('sistema', 'Sistema'),
    ]

    processo = models.ForeignKey(Processo, on_delete=models.PROTECT, related_name='movimentacoes', null=True, blank=True)
    descricao = models.TextField(null=True, blank=True)
    realizado_por = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    realizado_em = models.DateTimeField(auto_now_add=True, db_index=True, null=True, blank=True)
    remetente = models.ForeignKey(SetorHome, on_delete=models.PROTECT, related_name='SetorRemetente', null=True, blank=True)
    destinatario = models.ForeignKey(SetorHome, on_delete=models.PROTECT, related_name='SetorDestinatario', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_tramitacao', null=True, blank=True)
    confirmacao = models.CharField(max_length=20, choices=RECEBIMENTO_CHOICES, default='pendente', null=True, blank=True)
    confirmado_em = models.DateTimeField(null=True, blank=True)
    confirmado_por = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='movimentacoes_confirmadas')
    observacoes = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        if self.status != 'arquivada':
            return f"Movimentação de {self.processo.numero} para {self.destinatario.nome} realizada por {self.realizado_por}"
        else:
            return f"Movimentação para arquivo do {self.processo.numero} realizada por {self.realizado_por}"

    def clean(self):
        if self.remetente == self.destinatario:
            raise ValidationError("O setor de origem não pode ser o mesmo que o setor de destino.")
        
        if self.remetente == self.destinatario:
            raise ValidationError("O setor de origem não pode ser o mesmo que o setor de destino.")

    def save(self, *args, **kwargs):
        """
        Atualiza a última movimentação do processo ao salvar uma nova movimentação.
        """
        super().save(*args, **kwargs)
        self.processo.ultima_movimentacao = self
        self.processo.atual = self.destinatario
        self.processo.save()

class ProtocoloMovimentacao(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente de Anexo'),
        ('confirmado', 'Confirmado'),
    ]

    movimentacoes = models.ManyToManyField(Movimentacao, related_name='protocolos')
    destinatario = models.ForeignKey(SetorHome, on_delete=models.PROTECT, null=True, blank=True, default=None, related_name='SetoresDestinatarios')
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    comprovacao = models.FileField(upload_to=diretorioProtocolo, blank=True, null=True)

    def __str__(self):
        return f"Protocolo {self.id} - {self.destinatario.nome}"

    def confirmar(self):
        """
        Confirma o protocolo e atualiza o status das movimentações.
        """
        self.status = 'confirmado'
        self.save()
        self.movimentacoes.update(status='recebida', confirmacao='manual')

class CorrecaoProcesso(models.Model):

    CAMPOS_CHOICES = [
        ("numero", "Número"),
        ("titulo", "Título"),
        ("descricao", "Descrição"),
        ("fim", "Setor Fim"),
    ]

    processo = models.ForeignKey(Processo, on_delete=models.CASCADE, related_name='correcoes')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now_add=True)

    campo_alterado = models.CharField(max_length=50, choices=CAMPOS_CHOICES)  # ex: 'título', 'setor_destino'
    valor_anterior = models.TextField()
    valor_novo = models.TextField()

    def __str__(self):
        return f"Correção do campo '{self.campo_alterado}' por {self.usuario.get_full_name}"