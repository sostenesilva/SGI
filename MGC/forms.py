from django import forms
from . import models

# class Contratos_form (forms.ModelForm):
#     class Meta:
#         model = models.Contratos
#         fields = ('n_contrato','ano_contrato','inicio_vigencia','fim_vigencia','razao_social', 'num_documento','valor')

#         widgets = {
#             'n_contrato': forms.NumberInput(attrs={'class':'form-control'}),
#             'ano_contrato': forms.NumberInput(attrs={'class':'form-control'}),
#             'inicio_vigencia': forms.DateInput(attrs={'class':'form-control'}),
#             'fim_vigencia': forms.DateInput(attrs={'class':'form-control'}),
#             'razao_social': forms.TextInput(attrs={'class':'form-control'}),
#             'num_documento': forms.TextInput(attrs={'class':'form-control'}),
#             'valor': forms.NumberInput(attrs={'class':'form-control'}),
#         }

class Ordem_form (forms.ModelForm):
    class Meta:
        model = models.Ordem
        fields = '__all__'

        widgets = {
            'valor': forms.NumberInput(attrs={'class':'form-control'}),
            'arquivo': forms.FileInput(attrs={'class':'form-control','rows':'5', 'name':'arquivo'}),
        }

class SaldoContratoSec_form (forms.ModelForm):
    class Meta:
        model = models.SaldoContratoSec
        fields = ('sec','fiscal',)

        widgets = {
            'sec': forms.Select(attrs={'class':'form-control'}),
            'fiscal': forms.Select(attrs={'class':'form-control'}),
        }

class Fornecedor_form (forms.ModelForm):
    class Meta:
        model = models.Fornecedores
        fields = ('RazaoSocial','NumeroDocumentoAjustado','Endereco','Representante','Contato','Email')

        widgets = {
            'RazaoSocial': forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),
            'NumeroDocumentoAjustado': forms.TextInput(attrs={'class':'form-control','readonly':'readonly'}),
            'Endereco': forms.TextInput(attrs={'class':'form-control'}),
            'Representante': forms.TextInput(attrs={'class':'form-control'}),
            'Contato': forms.TextInput(attrs={'class':'form-control'}),
            'Email': forms.EmailInput(attrs={'class':'form-control'}),
        }

class EntradaIten (forms.ModelForm):
    class Meta:
        model = models.EntradaSec
        fields = ('quantidade',)








# class Avaliacao_form (forms.ModelForm):
#     class Meta:
#         model = Db_Avaliacao
#         fields = ('criterio','responsavel', 'data_limite','status')

#         widgets = {
#             'criterio': forms.Select(attrs={'class':'form-control'}),
#             'responsavel': forms.Select(attrs={'class':'form-control'}),
#             'data_limite': forms.DateInput(attrs={'class':'form-control'}),
#             'status': forms.Select(attrs={'class':'form-control'}),
#         }

# class Email_group_form (forms.ModelForm):
#     class Meta:
#         model = Email_group
#         fields = ('group','email_group')

#         widgets = {
#             'group': forms.Select(attrs={'class':'form-control form-sm'}),
#             'email_group': forms.EmailInput(attrs={'class':'form-control form-sm'}),
#         }