from django import forms

from .models import OtelOda


class UpdateOtelOdaForm(forms.ModelForm):

    class Meta:
        model = OtelOda
        fields = ["odaNumarasi","odaTipi","odaTemizMi","odaArizaliMi","odaBosMu","odaProblemi"]