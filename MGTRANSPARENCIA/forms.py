from django import forms
from .models import DbAvaliacaoLog

class AvaliacaoLogForm(forms.ModelForm):
    class Meta:
        model = DbAvaliacaoLog
        fields = ["arquivo", "anotacao"]

        widgets = {
            "arquivo": forms.FileInput(attrs={"class": "form-control"}),
            "anotacao": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
