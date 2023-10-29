from django import forms

from .models import OtelOda, KonukBilgileri


class UpdateOtelOdaForm(forms.ModelForm):

    class Meta:
        model = OtelOda
        fields = ["odaNumarasi","odaTipi","odaTemizMi","odaArizaliMi","odaBosMu","odaProblemi"]


class UpdateMusteriDetay(forms.ModelForm):

    class Meta:
        model = KonukBilgileri
        fields = ["musteriNotu"]