from django.db import models


# User Modelini çek
from django.contrib.auth.models import User

# Integerfieldlar için Validators
from django.core import validators
# Validator Error İçin
from django.core.exceptions import ValidationError


# Create your models here.

class OtelYonetim(models.Model):
    owner = models.ForeignKey(User, verbose_name=("Otel Sahibi"), on_delete=models.CASCADE)
    title = models.CharField(("Otel Adı"), max_length=50)
    image = models.ImageField(("Otel Logosu"), upload_to="Logo", height_field=None, width_field=None, max_length=None)
    address = models.CharField(("Otel Adresi"), max_length=50)
    telephone = models.CharField(("Otel Telefon Numarası"), max_length=13)

    def __str__(self) -> str:
        return self.title

class OtelOda(models.Model):
    otel = models.ForeignKey(OtelYonetim, verbose_name=("Otel Adı"), on_delete=models.CASCADE)
    odaNumarasi = models.CharField(("Oda Numarası"), max_length=5)
    odaTipi = models.CharField(("Oda Tipi"), max_length=50)
    odaFiyat = models.DecimalField(("Oda Fiyatı"), default=000.00, max_digits=10, decimal_places=2, blank=True)
    odaTemizMi = models.BooleanField(("Oda Temiz Mi?"), default=True, blank=True)
    odaArizaliMi = models.BooleanField(("Oda Arızalı Mı?"), default=False, blank=True)
    odaRezerveMi = models.BooleanField(('Oda Rezerve Mi?'), default=False, blank=True)
    odaBosMu = models.BooleanField(("Oda Boş Mu?"), default=True, blank=True)
    odaProblemi = models.TextField(("Odanın Problemi Nedir?"), max_length=500, blank=True)

    def __str__(self) -> str:
        return self.odaNumarasi
