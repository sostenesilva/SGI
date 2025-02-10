from datetime import date
import os
from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError

def diretorioDocumento (instance, filename):
    return f'MGPROTOCOLO/documentos/{instance.processo.criado_em.year}/{instance.processo.setor_demandante.nome}/{instance.processo.numero}/{filename}'

def diretorioProtocolo (instance, filename):
    extensao = os.path.splitext(filename)[1]
    return f'MGPROTOCOLO/protocolos/{instance.criado_em.year}/{instance.setor_destino.nome}/{instance.criado_em} por {instance.criado_por.username} - id {instance.id}{extensao}'

class Setor(models.Model):
    nome = models.CharField(max_length=255, unique=True, null=True, blank=True)
    sigla = models.CharField(max_length=10, blank=True, null=True)
    usuarios = models.ManyToManyField(User, related_name='setores', null=True, blank=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Processo(models.Model):
    STATUS_CHOICES = [
        ('em_analise', 'Em análise'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    numero = models.CharField(max_length=100, unique=True, db_index=True, null=True, blank=True)
    titulo = models.CharField(max_length=255, null=True, blank=True)
    descricao = models.TextField(blank=True, null=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    setor_demandante = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True, blank=True, related_name='processos_demandantes')
    setor_fim = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True, blank=True, related_name='processos_setorfim')
    setor_atual = models.ForeignKey(Setor, on_delete=models.SET_NULL, null=True, blank=True, related_name='processos_setoratual')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_analise', null=True, blank=True)
    prazo = models.DateField(blank=True, null=True)
    criado_em = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    atualizado_em = models.DateTimeField(auto_now=True, null=True, blank=True)
    ultima_movimentacao = models.ForeignKey('Movimentacao', on_delete=models.SET_NULL, null=True, blank=True, related_name='processo_ultima_movimentacao')
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.numero} - {self.titulo}"

    def clean(self):
        if self.setor_demandante == self.setor_fim:
            raise ValidationError("O setor demandante não pode ser o mesmo que o setor responsável.")

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
                'setor_origem': movimentacao.setor_origem.nome,
                'setor_destino': movimentacao.setor_destino.nome,
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
            setores.add(movimentacao.setor_origem.nome)
            setores.add(movimentacao.setor_destino.nome)
        return list(setores)

    @classmethod
    def processos_no_setor(cls, setor):
        """
        Retorna os processos cuja última movimentação está no setor especificado.
        """
        return cls.objects.filter(setor_atual=setor)

    @classmethod
    def processos_encaminhados_pelo_setor(cls, setor):
        """
        Retorna os processos que foram encaminhados pelo setor especificado para outros setores.
        """
        return cls.objects.filter(movimentacoes__setor_origem=setor).distinct()
    
    def usuario_pode_modificar(self, usuario):
        """
        Verifica se o usuário pertence ao setor atual do processo.
        """
        return usuario in self.setor_atual.usuarios.all() if self.setor_atual else False

class Documento(models.Model):
    TIPO_CHOICES = [
        ('inicial', 'Documento Inicial'),
        ('complementar', 'Documento Complementar'),
    ]

    CLASSIFICACAO_CHOICES = [
        ('oficio', 'Ofício'),
        ('ci', 'Comunicado Interno'),
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
    setor_origem = models.ForeignKey(Setor, on_delete=models.PROTECT, related_name='movimentacoes_origem', null=True, blank=True)
    setor_destino = models.ForeignKey(Setor, on_delete=models.PROTECT, related_name='movimentacoes_destino', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='em_tramitacao', null=True, blank=True)
    confirmacao = models.CharField(max_length=20, choices=RECEBIMENTO_CHOICES, default='pendente', null=True, blank=True)
    confirmado_em = models.DateTimeField(null=True, blank=True)
    confirmado_por = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True, related_name='movimentacoes_confirmadas')
    observacoes = models.TextField(blank=True, null=True)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"Movimentação para {self.setor_destino.nome} em {self.processo.numero} por {self.realizado_por}"

    def clean(self):
        if self.setor_origem == self.setor_destino:
            raise ValidationError("O setor de origem não pode ser o mesmo que o setor de destino.")

    def save(self, *args, **kwargs):
        """
        Atualiza a última movimentação do processo ao salvar uma nova movimentação.
        """
        super().save(*args, **kwargs)
        self.processo.ultima_movimentacao = self
        self.processo.setor_atual = self.setor_destino
        self.processo.save()

class ProtocoloMovimentacao(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente de Anexo'),
        ('confirmado', 'Confirmado'),
    ]

    movimentacoes = models.ManyToManyField(Movimentacao, related_name='protocolos')
    setor_destino = models.ForeignKey(Setor, on_delete=models.PROTECT, related_name='protocolos_recebidos')
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    comprovacao = models.FileField(upload_to=diretorioProtocolo, blank=True, null=True)

    def __str__(self):
        return f"Protocolo {self.id} - {self.setor_destino.nome}"

    def confirmar(self):
        """
        Confirma o protocolo e atualiza o status das movimentações.
        """
        self.status = 'confirmado'
        self.save()
        self.movimentacoes.update(status='recebida', confirmacao='manual')