from django.core.management.base import BaseCommand
from django.utils import timezone
from MGTRANSPARENCIA.models import DbAvaliacaoLog
from datetime import timedelta

class Command(BaseCommand):
    help = 'Atualiza tarefas pendentes para atrasadas se a data limite passou'

    def handle(self, *args, **kwargs):
        ## A data limite da tarefa tem hora 00:00, por isso o deslocamento de 1 dia na data atual.
        agora = timezone.now()

        tarefas_atrasadas = DbAvaliacaoLog.objects.filter(
            status='Pendente',
            data_limite__lt=agora - timedelta(days=1)
        )
        count = tarefas_atrasadas.count()
        tarefas_atrasadas.update(status='Atrasado')

        self.stdout.write(self.style.SUCCESS(f'Data atual: {agora} - {count} tarefas marcadas como atrasadas.'))
