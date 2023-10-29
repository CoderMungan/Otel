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
    odaTemizMi = models.BooleanField(("Oda Temiz Mi?"), default=True, blank=True)
    odaArizaliMi = models.BooleanField(("Oda Arızalı Mı?"), default=False, blank=True)
    odaRezerveMi = models.BooleanField(('Oda Rezerve Mi?'), default=False, blank=True)
    odaBosMu = models.BooleanField(("Oda Boş Mu?"), default=True, blank=True)
    odaProblemi = models.TextField(("Odanın Problemi Nedir?"), max_length=500, blank=True)

    def __str__(self) -> str:
        return self.odaNumarasi


class KonukBilgileri(models.Model):
    otel = models.ForeignKey(OtelYonetim, verbose_name=("Otel Adı"), on_delete=models.CASCADE)
    firstname = models.CharField(("Müşterinin Adı"), max_length=50)
    lastname = models.CharField(("Müşterinin Soyadı"), max_length=50)
    uyrugu = models.CharField(("Müşterinin Uyruğu"), max_length=50)
    musteriTC = models.CharField(("Müşteri TC Numarası"), max_length=11, blank=True)
    musteriID = models.CharField(("Müşteri Passaport Numarası"), max_length=50, blank = True)
    musteriNotu = models.TextField(("Müşteri Notu"), max_length=250, default="", blank=True)


    def __str__(self) -> str:
        return self.firstname + " " + self.lastname
    

class KonukCheckInveCheckOut(models.Model):
    otel = models.ForeignKey(OtelYonetim, verbose_name=("Otel Adı"), on_delete=models.CASCADE)
    konuk = models.ForeignKey(KonukBilgileri, verbose_name=("Konuk Bilgileri"), on_delete=models.CASCADE)
    oda = models.ForeignKey(OtelOda, verbose_name=("Otel Oda"), on_delete=models.CASCADE)
    checkIn = models.DateTimeField(("Check-In Zamanı"), auto_now=False, auto_now_add=False)
    checkOut = models.DateTimeField(("Check-Out Zamanı"), auto_now=False, auto_now_add=False)
    fiyat = models.DecimalField(("Fiyat"), max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return self.konuk