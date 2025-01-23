from django.shortcuts import render, get_object_or_404
from .models import Modulo
from django.contrib.auth.decorators import login_required


@login_required
def portal_inicial(request):
    modulos = Modulo.objects.all()
    return render(request, 'portal_inicial.html', {'modulos': modulos})

login_required
def modulo_detalhes(request, modulo_id):
    modulo = get_object_or_404(Modulo, pk=modulo_id)
    return render(request, 'modulo_detalhes.html', {'modulo': modulo})
