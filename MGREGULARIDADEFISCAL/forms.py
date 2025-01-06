from django import forms
from . import models

class Certidoes_form(forms.ModelForm):
    class Meta:
        model = models.Certidao
        fields = ('fornecedor','tipo','dataEmissao','dataValidade','autenticacao', 'autor', 'arquivo')

        widgets = {
            'fornecedor': forms.HiddenInput(),
            'autor': forms.HiddenInput(),
            'tipo': forms.HiddenInput(),
            'dataEmissao': forms.DateInput(attrs={'class':'form-control form-control-sm','placeholder':'Emissão'}),
            'dataValidade': forms.DateInput(attrs={'class':'form-control form-control-sm','placeholder':'Validade'}),
            'autenticacao': forms.TextInput(attrs={'class':'form-control form-control-sm','placeholder':'Autenticação'}),
            'arquivo': forms.FileInput(attrs={'class':'form-control form-control-sm'}),
        }