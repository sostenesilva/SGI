from django.shortcuts import render, get_object_or_404
from .models import Modulo

def portal_inicial(request):
    modulos = Modulo.objects.all()
    return render(request, 'portal_inicial.html', {'modulos': modulos})

def modulo_detalhes(request, modulo_id):
    modulo = get_object_or_404(Modulo, pk=modulo_id)
    return render(request, 'modulo_detalhes.html', {'modulo': modulo})
