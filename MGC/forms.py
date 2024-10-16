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
        fields = ('valor','arquivo')

        widgets = {
            'valor': forms.NumberInput(attrs={'class':'form-control'}),
            'arquivo': forms.FileInput(attrs={'class':'form-control','rows':'5', 'name':'arquivo'}),
        }

class SaldoSec_form (forms.ModelForm):
    class Meta:
        model = models.EntradaSec
        fields = ('sec',)

        widgets = {
            'sec': forms.Select(attrs={'class':'form-control'}),
        }

class Fiscal_form (forms.ModelForm):
    class Meta:
        model = models.SaldoContratoSec
        fields = ('fiscal',)

        widgets = {
            'fiscal': forms.Select(attrs={'class':'form-control'}),
        }


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