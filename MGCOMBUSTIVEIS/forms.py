from django import forms
from . import models

class Frota_form(forms.ModelForm):
    class Meta:
        model = models.veiculo
        fields = '__all__'

        widgets= {
            'placa':forms.TextInput(attrs={'class':'form-control', 'type':'text','placeholder':'Ex.: ABC1234', 'required':'True'}),
            'ano':forms.TextInput(attrs={'class':'form-control', 'type':'number','placeholder':'Ex.: 2023'}),
            'modelo':forms.TextInput(attrs={'class':'form-control', 'type':'text','placeholder':'Ex.: Amarok'}),
            'secretaria':forms.Select(attrs={'class':'form-select'}),
            'descricao':forms.Textarea(attrs={'class':'form-control', 'type':'text', 'rows':'2', 'placeholder':'Detalhes sobre o veículo'}),
            'status':forms.Select(attrs={'class':'form-select'}),
            'propriedade':forms.Select(attrs={'class':'form-select'}),
            'observacao':forms.Textarea(attrs={'class':'form-control', 'rows':'2'})
        }

class Condutores_form(forms.ModelForm):
    class Meta:
        model = models.condutor
        fields = '__all__'

        widgets= {
            'nome':forms.TextInput(attrs={'class':'form-control', 'type':'text','placeholder':'Nome completo', 'required':'True'}),
            'cpf':forms.TextInput(attrs={'class':'form-control', 'type':'text','placeholder':'XXX.XXX.XXX-XX', 'required':'True'}),
            'status':forms.Select(attrs={'class':'form-select'}),
            'validadeCNH':forms.DateInput(format=('%Y-%m-%d'),attrs={'class':'form-control', 'type':'date'}),
            'categoriaCNH':forms.TextInput(attrs={'class':'form-control', 'type':'text', 'placeholder':"Ex.: AB, C"}),
            'cursoEscolar':forms.CheckboxInput(attrs={'class':'form-check-input', 'type':'checkbox','placeholder':'Ex.: 6,49'}),
            'observacoes':forms.Textarea(attrs={'class':'form-control', 'rows':'2'})
        }

class Abastecimentos_form(forms.ModelForm):
    class Meta:
        model = models.Abastecimentos
        fields = '__all__'
    
        widgets= {
            'veiculo':forms.Select(attrs={'class':'form-control'}),
            'condutor':forms.Select(attrs={'class':'form-control'}),
            'fiscal':forms.Select(attrs={'class':'form-control'}),
            'data':forms.DateInput(format=('%Y-%m-%d'), attrs={'class':'form-control', 'type':'date', 'required':'True'}),
            'tipo':forms.Select(attrs={'class':'form-select', 'required':'True'}),
            'valorUnitario':forms.NumberInput(attrs={'class':'form-control', 'required':'True', 'type':'number','placeholder':'Ex.: 6,49'}),
            'quantidade':forms.NumberInput(attrs={'class':'form-control', 'required':'True', 'type':'number','placeholder':'Ex.: 50,5'}),
            'valorTotal':forms.NumberInput(attrs={'class':'form-control', 'required':'True', 'type':'number','placeholder':'Ex.: 324,50'}),
            'km':forms.NumberInput(attrs={'class':'form-control', 'type':'number','placeholder':'Ex.: 15000'}),
            'status':forms.Select(attrs={'class':'form-select', 'required':'True'}),
        }