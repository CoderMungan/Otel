from .models import *
from django.utils import timezone
from django.shortcuts import redirect
from datetime import datetime, date

def odaDurumuDegistir():

    guncel_zaman = timezone.now()

    checkouts = KonukCheckInveCheckOut.objects.filter(checkOut__lt = guncel_zaman)
    checkins = KonukCheckInveCheckOut.objects.filter(checkIn__gte = guncel_zaman)

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

def odastatus(kisi,odaID):

    oda = OtelOda.objects.filter(id = odaID).first()
    guncel_zaman = timezone.now()

    checkoutBuyuk = KonukCheckInveCheckOut.objects.filter(oda = oda, checkIn__gt = guncel_zaman).all()
    checkoutKucuk = KonukCheckInveCheckOut.objects.filter(oda = oda, checkIn__lte = guncel_zaman).all()

    for kisi in checkoutKucuk:
        kisi.oda.odaBosMu = False
        kisi.oda.save()
        print("Oda Doludur!")

    for kisi in checkoutBuyuk:
        kisi.oda.odaRezerveMi = True
        kisi.oda.save()
        print("Oda Rezerve Olmuştur")


    # print("Kişi Çekin: ",kisi.checkIn)

    # datetime_object = datetime.strptime(kisi.checkIn, '%Y-%m-%dT%H:%M')
    # print("datetime: ", datetime_object)
    # tarih = date(datetime_object.year,datetime_object.month,datetime_object.day)
    # print("Tarih Değişkeni: ", tarih)

    # if tarih == datetime.today():
    #     oda.odaBosMu = False
    #     oda.save()
    #     print("Oda Doludur!")
    # elif tarih > datetime.today():
    #     oda.odaRezerveMi = True
    #     oda.save()
    #     print("Oda Rezerve Olmuştur!")

    # print("Nasıl geliyor: ", kisi.checkIn)
    # print("Güncel Zaman:", guncel_zaman)

    # if kisi.checkIn <= guncel_zaman:
    #     oda.odaBosMu = False
    #     oda.save()
    #     print("Oda Durumu Değişmiştir!")
    # else:
    #     oda.odaRezerveMi = True
    #     oda.save()
    #     print("Oda Rezerve Olmuştur!")
