from django import forms

from .models import OtelOda, KonukBilgileri, KonukCheckInveCheckOut


class UpdateOtelOdaForm(forms.ModelForm):

    class Meta:
        model = OtelOda
        fields = ["odaNumarasi","odaTipi","odaTemizMi","odaArizaliMi","odaBosMu","odaProblemi",]


class UpdateMusteriDetay(forms.ModelForm):

    class Meta:
        model = KonukBilgileri
        fields = ["musteriNotu"]


class UpdateBlokaj(forms.ModelForm):

    class Meta:
            model = KonukCheckInveCheckOut
            options = [('#be3228','Kırmızı'),('#3d85c6','Mavi'),('#02e107','Yeşil'),('#800080','Pembe'),('#083516','Koyu Yeşil'),('#331387','Mor')]
            fields = ["konuk","oda","checkIn","checkOut","color"]
            widgets = {
                'checkIn': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                'checkOut': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                'color': forms.Select(choices=options)
            }