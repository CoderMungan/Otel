from django.shortcuts import render,redirect

# Müsti Abi
import traceback


# TimeZone
from django.utils import timezone

# CronJob
from .cronjob import start_jobs
from .jobs import *

# ObjeYokİse
from django.core.exceptions import ObjectDoesNotExist

# Djangonun User Modelini
from django.contrib.auth.models import User
# Mekanikler
from django.contrib.auth import authenticate, login, logout

# Kendi Model ORM
from .models import *

# MiddleWare
from django.contrib.auth.decorators import login_required

# Form'ları Çağır
from .forms import *

# Message Çek
from django.contrib import messages

# Create your views here.

def anasayfa(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if username and password:
            userLogin = authenticate(request, username = username, password = password)
            
            if userLogin is not None:
                login(request,userLogin)
                # Message Geç
                messages.success(request, "Giriş Başarılı!")
                return redirect('dashboard')
            else:
                # Message Geç
                messages.error(request, "Kullanici adi veya sifre hatalidir.")
                return redirect('anasayfa')
        else:
            # Message Geç
            messages.warning(request,"Boşlukları Lütfen Doldurunuz!")
            return redirect('anasayfa')


    return render(request, 'index.html')


# Dashboard sayfasıdır
@login_required(login_url="anasayfa")
def dashboard(request):

    context = {}

    otel = OtelYonetim.objects.filter(owner = request.user).first()
    oda = OtelOda.objects.filter(otel = otel).all()
    context['odalar'] = oda

    checkinout = KonukCheckInveCheckOut.objects.filter(otel = otel).all()
    context['musteriler'] = checkinout

    return render(request,'dashboard.html', context)


@login_required(login_url="anasayfa")
def odaEkle(request):

    otel = OtelYonetim.objects.filter(owner = request.user).first()

    if request.method == "POST":
        odatipi = request.POST.get('room-tipi')
        odanumarasi = request.POST.get('room-numarasi')
        if odatipi and odanumarasi:
            yeniOda = OtelOda.objects.create(otel = otel, odaNumarasi = odanumarasi, odaTipi = odatipi )
            if yeniOda is None:
                messages.error(request, "Bilinmeyen bir hatadan dolayi Odayi eklenemedi.")
                return redirect('dashboard')
            else:
                return redirect('dashboard')
        else:
            messages.warning(request,"Lutfen Tüm Alanları Doldurunuz!")
    
    return redirect('dashboard')


@login_required(login_url="anasayfa")
def misafirekle(request, odaID):

    otel = OtelYonetim.objects.filter(owner = request.user).first()
    oda = OtelOda.objects.filter(id = odaID).first()
    
    if request.user:
        if request.method == "POST":
            firstname = request.POST.get('first')
            lastname = request.POST.get('last')
            uyruk = request.POST.get('uyruk')
            tckimlik = request.POST.get('tc')
            passaport = request.POST.get('passaport')
            musterinotu = request.POST.get('guest_note')
            musterifiyat = request.POST.get('price')
            musteriparabirimi = request.POST.get('parabirimi')
            checkin = request.POST.get('checkin')
            checkout = request.POST.get('checkout')
            if firstname and lastname and uyruk and musterifiyat and checkin and checkout:
                if tckimlik or passaport:
                    KonukBilgileri.objects.create(otel = otel, firstname = firstname, lastname = lastname, uyrugu = uyruk, musteriTC = tckimlik, musteriID = passaport, musteriNotu = musterinotu, fiyat = musterifiyat, kur = musteriparabirimi)
                    # Kayıt sonrası kişi bilgilerini çek
                    kisi = KonukBilgileri.objects.filter(otel = otel, firstname = firstname, lastname = lastname).first()
                    KonukCheckInveCheckOut.objects.create(otel = otel, konuk = kisi, oda = oda, checkIn = checkin, checkOut = checkout)
                    oda.odaBosMu = False
                    oda.save()
                    messages.success(request, "Müşteri başarıyla kaydedilmiştir!")
                    return redirect('odadetay', odaID)
        else:
            return redirect('404')
    else:
        messages.error(request, "Lütfen Giriş Yapınız!")
        return redirect('404')


@login_required(login_url="anasayfa")
def odadetay(request,odaID):

    context = {}

    misafir = KonukCheckInveCheckOut.objects.filter(oda__id = odaID).first()
    context['misafir'] = misafir
    try:
        ilgiliOda = OtelOda.objects.get(id = odaID)
        context['ilgiliOda'] = ilgiliOda
        ilgiliOdaForm = UpdateOtelOdaForm(instance = ilgiliOda)
        context['form'] = ilgiliOdaForm

        if request.method == "POST":
            form = UpdateOtelOdaForm(request.POST,instance = ilgiliOda)
            if form.is_valid():
                form.save()
                return redirect('odadetay', odaID)
            else:
                messages.error(request,"Hatalı Veri Girişi Olmuştur.")
    # except Exception as a:
    except OtelOda.DoesNotExist:
        # Exceptionsların hatasını konsola basar
        # traceback.print_exc()
        return redirect('404')

    return render(request, "odadetay.html",context)


# Blokaj sayfası
@login_required(login_url='anasayfa')
def blokaj(request):
    context = {}
    odalar = OtelOda.objects.all()
    context["odalar"] = odalar
    return render(request, 'blokaj.html', context)



@login_required(login_url='anasayfa')
def odasil(request,odaID):

    oda = OtelOda.objects.filter(id = odaID).first()

    if oda and request.user:
        oda.delete()
        messages.success(request, f'{oda} Numaralı Oda Başarıyla Silindi')
        return redirect('dashboard')
    else:
        return redirect('404')
    

# Misafir Detay
@login_required(login_url='anasayfa')
def misafirdetay(request,misafirID):

    context = {}
    konuk = KonukBilgileri.objects.filter(id = misafirID).first()
    context['kisi'] = konuk
    girisCikis = KonukCheckInveCheckOut.objects.filter(konuk = konuk).first()
    context['cikisgiris'] = girisCikis
    musteriForm = UpdateMusteriDetay(instance=konuk)
    context["musteriform"] = musteriForm

    if request.method == "POST":
        form = UpdateMusteriDetay(request.POST, instance=konuk)
        if form.is_valid():
            form.save()
            messages.success(request, "Müşteriye not başarıyla eklendi!")
            return redirect("misafirdetay", misafirID)

    return render(request, 'misafirdetay.html', context)

@login_required(login_url='anasayfa')
def checkoutyaptir(request,misafirID):
    checkoutislemi = KonukCheckInveCheckOut.objects.filter(konuk__id = misafirID).first()
    
    if checkoutislemi and request.user.is_authenticated:
        checkoutislemi.delete()
        return redirect('dashboard')
    else:
        return redirect('404')



# Muhasebe
@login_required(login_url='anasayfa')
def muhasebe(request):
    return render(request,'muhasebe.html')

# Logout Sayfasıdır
@login_required(login_url="anasayfa")
def cikisYap(request):
    logout(request)
    return redirect('anasayfa')


# 404 Sayfası
def hatasayfasi(request):
    return render(request, '404.html')