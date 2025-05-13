from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from HOME.models import Secretaria, Setor

class Demanda(models.Model):
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    documento_motivador = models.CharField(max_length=255)
    prazo_geral = models.DateField(blank=True, null=True)
    criada_por = models.ForeignKey(User, on_delete=models.PROTECT)
    criada_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo

class Diligencia(models.Model):
    demanda = models.ForeignKey(Demanda, on_delete=models.CASCADE, related_name="diligencias")
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    setor_responsavel = models.ForeignKey(Setor, on_delete=models.PROTECT)
    prazo = models.DateField(blank=True, null=True)
    tipo = models.CharField(
        max_length=20,
        choices=[
            ('demanda', 'Demanda'),
            ('resposta', 'Resposta'),
            ('encaminhamento', 'Encaminhamento'),
            ('ciencia', 'Ciência')
        ],
        default='demanda'
    )
    status = models.CharField(
        max_length=20,
        choices=[
            ('pendente', 'Pendente'),
            ('concluida', 'Concluída'),
            ('atrasada', 'Atrasada')
        ],
        default='pendente'
    )
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    criado_em = models.DateTimeField(auto_now_add=True)

    def esta_atrasada(self):
        from django.utils import timezone
        return self.status == 'pendente' and self.prazo and self.prazo < timezone.localdate()

    def __str__(self):
        return self.titulo

class HistoricoDiligencia(models.Model):
    diligencia = models.ForeignKey(Diligencia, on_delete=models.CASCADE, related_name='historico')
    observacao = models.TextField()
    criado_por = models.ForeignKey(User, on_delete=models.PROTECT)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Histórico em {self.criado_em.strftime('%d/%m/%Y')} por {self.criado_por.get_full_name()}"
