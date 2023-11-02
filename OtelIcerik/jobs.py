from .models import *
from django.utils import timezone
from django.shortcuts import redirect

def odaDurumuDegistir():

    guncel_zaman = timezone.now()

    checkouts = KonukCheckInveCheckOut.objects.filter(checkOut__lt = guncel_zaman)

    if checkouts:
        for cikisOdadurumuDegisti in checkouts:
            oda = cikisOdadurumuDegisti.oda
            oda.odaBosMu = True
            oda.save()
            print(f'Oda {oda.odaNumarasi} artık boştur!')
            cikisOdadurumuDegisti.delete()

    print("CheckOut Kontrol Modülü Devrede!")