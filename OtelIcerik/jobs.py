from datetime import date, datetime
from django.shortcuts import redirect
from django.utils import timezone

from .models import *


def odaDurumuDegistir():
    guncel_zaman = timezone.now()

    checkouts = KonukCheckInveCheckOut.objects.filter(checkOut__lt=guncel_zaman)
    checkins = KonukCheckInveCheckOut.objects.filter(checkIn__gte=guncel_zaman)

    if checkins:
        for odaGiris in checkins:
            oda = odaGiris.oda
            oda.odaRezerveMi = True
            oda.save()
            print(f"Oda {oda.odaNumarasi}'nın Blokajlanmıştır!")

    if checkouts:
        for cikisOdadurumuDegisti in checkouts:
            oda = cikisOdadurumuDegisti.oda
            oda.odaBosMu = True
            oda.save()
            print(f"Oda {oda.odaNumarasi} artık boştur!")
            cikisOdadurumuDegisti.delete()

    print("CheckIn Kontrol Modülü Devrede!")
    print("CheckOut Kontrol Modülü Devrede!")


# Mücahit Öğretti Luuwa "type hint"
def odastatus(kisi: KonukCheckInveCheckOut, odaID: int) -> None:

    oda = OtelOda.objects.filter(id=odaID).first()
    guncel_zaman = timezone.now()

    checkoutBuyuk = KonukCheckInveCheckOut.objects.filter(
        oda=oda, checkIn__gt=guncel_zaman
    ).all()
    checkoutKucuk = KonukCheckInveCheckOut.objects.filter(
        oda=oda, checkIn__lte=guncel_zaman
    ).all()

    for kisi in checkoutKucuk:
        kisi.oda.odaBosMu = False
        kisi.oda.save()
        print("Oda Doludur!")

    for kisi in checkoutBuyuk:
        kisi.oda.odaRezerveMi = True
        kisi.oda.save()
        print("Oda Rezerve Olmuştur")
