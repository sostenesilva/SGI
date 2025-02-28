from django import forms
from . import models

class AvaliacaoLogForm(forms.ModelForm):
    class Meta:
        model = models.DbAvaliacaoLog
        fields = ['arquivo','anotacao']

        widgets = {
            "arquivo": forms.FileInput(attrs={"class": "form-control"}),
            "anotacao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

class AvaliacaoForm (forms.ModelForm):
    class Meta:
        model = models.DbAvaliacao
        fields = '__all__'

        widgets = {
            "criterio": forms.Select(attrs={"class": "form-control"}),
            "responsavel": forms.Select(attrs={"class": "form-control"}),
            "secretaria": forms.Select(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-control"}),
        }