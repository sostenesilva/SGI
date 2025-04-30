from django.core.management.base import BaseCommand
from django.utils import timezone
from MGTRANSPARENCIA.models import DbAvaliacaoLog

class Command(BaseCommand):
    help = 'Atualiza tarefas pendentes para atrasadas se a data limite passou'

    def handle(self, *args, **kwargs):
        agora = timezone.now()
        tarefas_atrasadas = DbAvaliacaoLog.objects.filter(
            status='Pendente',
            data_limite__lt=agora
        )
        count = tarefas_atrasadas.count()
        tarefas_atrasadas.update(status='Atrasado')

        self.stdout.write(self.style.SUCCESS(f'{count} tarefas marcadas como atrasadas.'))
