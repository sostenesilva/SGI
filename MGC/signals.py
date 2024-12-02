from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from . import models

@receiver([post_save, post_delete], sender=models.EntradaSec)
def atualizar_saldo_entradas(sender, instance, **kwargs):
    saldocontratosec = instance.saldocontratosec
    entradas = saldocontratosec.entradas.all()  # Todas as entradas relacionadas
    total_entradas = sum([entrada.item.PrecoUnitario*entrada.quantidade for entrada in entradas])  # Soma os valores totais
    saidas = saldocontratosec.saidas.all()  # Todas as saídas relacionadas
    total_saidas = sum([saida.valor for saida in saidas])  # Soma as saídas

    saldocontratosec.totalEntradas = total_entradas  # Recalcula o saldo
    saldocontratosec.totalSaidas = total_saidas  # Recalcula o saldo
    saldocontratosec.saldoAtual = total_entradas - total_saidas  # Recalcula o saldo
    saldocontratosec.save()  # Salva a instância

@receiver([post_save, post_delete], sender=models.Ordem)
def atualizar_saldo_saidas(sender, instance, **kwargs):
    saldocontratosec = instance.saldoContratosec
    entradas = saldocontratosec.entradas.all()  # Todas as entradas relacionadas
    total_entradas = sum([entrada.item.PrecoUnitario*entrada.quantidade for entrada in entradas])  # Soma os valores totais
    saidas = saldocontratosec.saidas.all()  # Todas as saídas relacionadas
    total_saidas = sum([saida.valor for saida in saidas])  # Soma as saídas

    saldocontratosec.totalEntradas = total_entradas  # Recalcula o saldo
    saldocontratosec.totalSaidas = total_saidas  # Recalcula o saldo
    saldocontratosec.saldoAtual = total_entradas - total_saidas  # Recalcula o saldo
    saldocontratosec.save()  # Salva a instância