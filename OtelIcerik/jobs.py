from .models import *
from django.utils import timezone
from django.shortcuts import redirect

def odaDurumuDegistir():

    guncel_zaman = timezone.now()

    checkouts = KonukCheckInveCheckOut.objects.filter(checkOut__lt = guncel_zaman)
    checkins = KonukCheckInveCheckOut.objects.filter(checkIn__lt = guncel_zaman)

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
            print(f'Oda {oda.odaNumarasi} artık boştur!')
            cikisOdadurumuDegisti.delete()

    print("CheckIn Kontrol Modülü Devrede!")
    print("CheckOut Kontrol Modülü Devrede!")