from django import forms
from .models import Processo, Documento, Movimentacao, ProtocoloMovimentacao


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ImageForm(forms.ModelForm):
    photo = MultipleFileField(label='Select files', required=False)

class ProcessoForm(forms.ModelForm):

    documentos_iniciais = MultipleFileField(
        required=False,
        label="Documentos Iniciais"
    )

    class Meta:

        model = Processo
        fields = ['numero','titulo','descricao','fim', 'modalidade']

        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Ex: CI 001/2025/SASCF'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': "Ex: 'Solicitação de Liquidação', 'Contrato 005/2025 - HMR - Via Contabilidade'."}),
            'descricao': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': '3', 'placeholder': 'Ex: Número da nota, nome do fornecedor, período, número do contrato, nome do contratado, etc.'}),
            'fim': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'modalidade': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }

class ProcessoCorrecaoForm(forms.ModelForm):
    def __init__(self, *args, disabled=False, **kwargs):
        super().__init__(*args, **kwargs)
        if disabled:
            for field in self.fields.values():
                field.widget.attrs['disabled'] = True

    class Meta:
        model = Processo
        fields = ['numero','titulo','descricao','fim','modalidade']
        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Número do Processo (ex: CI 001/2025/SASCF)'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': "Título do Processo (ex: 'Solicitação de Liquidação')"}),
            'descricao': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': '3', 'placeholder': 'Descrição do Processo (ex: Número da nota, nome do fornecedor, período, número do contrato, nome do contratado, etc.)'}),
            'fim': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'modalidade': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['descricao','classificacao','arquivo']

        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Descrição do Documento'}),
            'classificacao': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'arquivo': forms.FileInput(attrs={'class': 'form-control form-control-sm', 'required':True}),
        }

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['descricao','destinatario']

        widgets = {
            'descricao': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': '3', 'placeholder': 'Descrição da Movimentação'}),
            'destinatario': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }

class ComprovacaoForm(forms.ModelForm):
    class Meta:
        model = ProtocoloMovimentacao
        fields = ['comprovacao']

        widgets = {
            'comprovacao': forms.FileInput(attrs={'class': 'form-control form-control-sm', 'required':True}),
        }