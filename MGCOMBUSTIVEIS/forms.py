from django import forms
from . import models


class Veiculo_form(forms.ModelForm):

    class Meta:
        model = models.veiculo
        fields = ('placa','secretaria','modelo','descricao','observacao')

        widgets = {
            'placa': forms.TextInput(attrs={'class':'form-control'}),
            'secretaria': forms.Select(attrs={'class':'form-control'}),
            'modelo': forms.TextInput(attrs={'class':'form-control'}),
            'descricao': forms.TextInput(attrs={'class':'form-control'}),
            'observacao': forms.TextInput(attrs={'class':'form-control'}),
        }

class Abastecimentos_form(forms.ModelForm):

    class Meta:
        model = models.Abastecimentos
        fields = ('data','veiculo','tipo','quantidade','valorUnitario','condutor','fiscal','km')

        widgets = {
            'data': forms.DateInput(attrs={'class':'form-control'}),
            'veiculo': forms.Select(attrs={'class':'form-control'}),
            'tipo': forms.TextInput(attrs={'class':'form-control'}),
            'quantidade': forms.TextInput(attrs={'class':'form-control'}),
            'valorUnitario': forms.NumberInput(attrs={'class':'form-control'}),
            'condutor': forms.Select(attrs={'class':'form-control'}),
            'fiscal': forms.Select(attrs={'class':'form-control'}),
            'km': forms.NumberInput(attrs={'class':'form-control'}),
        }