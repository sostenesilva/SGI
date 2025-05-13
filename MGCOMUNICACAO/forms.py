from django import forms
from .models import Demanda, Diligencia

class DemandaForm(forms.ModelForm):
    class Meta:
        model = Demanda
        fields = ['titulo','documento_motivador', 'descricao', 'prazo_geral']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'documento_motivador': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'prazo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

class DiligenciaForm(forms.ModelForm):
    class Meta:
        model = Diligencia
        fields = ['demanda', 'titulo', 'descricao', 'tipo', 'prazo']
        widgets = {
            'demanda': forms.HiddenInput(),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'prazo': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
