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
        fields = '__all__'

        widgets = {
            'numero': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Número do Processo'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Título do Processo'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': '3', 'placeholder': 'Descrição do Processo'}),
            'setor_demandante': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'setor_fim': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'setor_atual': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'status': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'prazo': forms.DateInput(attrs={'class': 'form-control form-control-sm', 'type': 'date'}),
            'criado_por': forms.HiddenInput(),  # Escondido, pois será preenchido automaticamente
        }

class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['descricao','classificacao','arquivo']

        widgets = {
            'descricao': forms.TextInput(attrs={'class': 'form-control form-control-sm', 'placeholder': 'Descrição do Documento'}),
            'classificacao': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'arquivo': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
        }

class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ['descricao','setor_destino']

        widgets = {
            'descricao': forms.Textarea(attrs={'class': 'form-control form-control-sm', 'rows': '3', 'placeholder': 'Descrição da Movimentação'}),
            'setor_destino': forms.Select(attrs={'class': 'form-control form-control-sm'}),
        }

class ComprovacaoForm(forms.ModelForm):
    class Meta:
        model = ProtocoloMovimentacao
        fields = ['comprovacao']

        widgets = {
            'comprovacao': forms.FileInput(attrs={'class': 'form-control form-control-sm'}),
        }