from django.shortcuts import render, redirect

#Deneme
from .decarator import *

# Müsti Abi
import traceback

# Utilities
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseRedirect

# Typing
import typing as t

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


RedirectOrResponse = t.Union[HttpResponseRedirect, HttpResponse]

@timing_decorator
def anasayfa(request: HttpRequest) -> RedirectOrResponse:
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        if username and password:
            userLogin = authenticate(request, username=username, password=password)

            if userLogin is not None:
                login(request, userLogin)
                # Message Geç
                messages.success(request, "Giriş Başarılı!")
                return redirect("dashboard")
            else:
                # Message Geç
                messages.error(request, "Kullanici adi veya sifre hatalidir.")
                return redirect("anasayfa")
        else:
            # Message Geç
            messages.warning(request, "Boşlukları Lütfen Doldurunuz!")
            return redirect("anasayfa")

    return render(request, "index.html")


# Dashboard sayfasıdır
@login_required(login_url="anasayfa")
def dashboard(request: HttpRequest) -> HttpResponse:
    context = {}

    otel = OtelYonetim.objects.filter(owner=request.user).first()
    oda = OtelOda.objects.filter(otel=otel).all()
    context["odalar"] = oda

    checkinout = KonukCheckInveCheckOut.objects.filter(otel=otel).all()
    context["musteriler"] = checkinout

    return render(request, "dashboard.html", context)


@login_required(login_url="anasayfa")
def odaEkle(request: HttpRequest) -> RedirectOrResponse:
    otel = OtelYonetim.objects.filter(owner=request.user).first()

    if request.user.is_authenticated:
        if request.method == "POST":
            odatipi = request.POST.get("room-tipi")
            odanumarasi = request.POST.get("room-numarasi")
            if odatipi and odanumarasi:
                yeniOda = OtelOda.objects.create(
                    otel=otel, odaNumarasi=odanumarasi, odaTipi=odatipi
                )
                if yeniOda is None:
                    messages.error(
                        request, "Bilinmeyen bir hatadan dolayi Odayi eklenemedi."
                    )
                    return redirect("dashboard")
                else:
                    messages.success(
                        request, f"Başarıyla {odanumarasi}'nolu odanız oluşturuldu!"
                    )
                    return redirect("dashboard")
            else:
                messages.error(request, "Boşlukları Lütfen Doldurunuz")
                return redirect("dashboard")
        return redirect("dashboard")
    else:
        return redirect("anasayfa")


@login_required(login_url="anasayfa")
def misafirekle(request: HttpRequest, odaID: int) -> RedirectOrResponse:
    otel = OtelYonetim.objects.filter(owner=request.user).first()
    oda = OtelOda.objects.filter(id=odaID).first()
    # Güvenlik Mekanizması
    if request.user.is_authenticated:
        # Form Yapısı
        if request.method == "POST":
            firstname = request.POST.get("first")
            lastname = request.POST.get("last")
            birthday = request.POST.get("dogumtarihi")
            uyruk = request.POST.get("uyruk")
            tckimlik = request.POST.get("tc")
            passaport = request.POST.get("passaport")
            musterinotu = request.POST.get("guest_note")
            musterifiyat = request.POST.get("price")
            musteriparabirimi = request.POST.get("parabirimi")
            checkin = request.POST.get("checkin")
            checkout = request.POST.get("checkout")
            if (
                firstname
                and lastname
                and uyruk
                and musterifiyat
                and checkin
                and checkout
            ):
                if tckimlik or passaport:
                    KonukBilgileri.objects.create(
                        otel=otel,
                        firstname=firstname,
                        lastname=lastname,
                        birthday=birthday,
                        uyrugu=uyruk,
                        musteriTC=tckimlik,
                        musteriID=passaport,
                        musteriNotu=musterinotu,
                        fiyat=musterifiyat,
                        kur=musteriparabirimi,
                    )
                    # Kayıt sonrası kişi bilgilerini çek
                    kisi = KonukBilgileri.objects.filter(
                        otel=otel, firstname=firstname, lastname=lastname
                    ).first()
                    checkOl = KonukCheckInveCheckOut.objects.create(
                        otel=otel,
                        konuk=kisi,
                        oda=oda,
                        checkIn=checkin,
                        checkOut=checkout,
                    )
                    messages.success(request, "Müşteri başarıyla kaydedilmiştir!")
                    # CronJob Devreye Sok
                    odastatus(checkOl, odaID)
                    return redirect("odadetay", odaID)
                else:
                    messages.error(request, "Lütfen Tc Kimliğini veya Passport ID'sini Giriniz!")
                    return redirect("odadetay", odaID)
            else:
                messages.error(request, "Lütfen Boşlukları Eksiksiz Doldurunuz!")
                return redirect("odadetay", odaID)
        else:
            return redirect("404")
    else:
        messages.error(request, "Lütfen Giriş Yapınız!")
        return redirect("anasayfa")


@login_required(login_url="anasayfa")
def odadetay(request: HttpRequest, odaID: int) -> RedirectOrResponse:
    context = {}
    misafir = KonukCheckInveCheckOut.objects.filter(oda__id=odaID).all()
    context["misafirler"] = misafir

    try:
        ilgiliOda = OtelOda.objects.get(id=odaID)
        context["ilgiliOda"] = ilgiliOda
        ilgiliOdaForm = UpdateOtelOdaForm(instance=ilgiliOda)
        context["form"] = ilgiliOdaForm
        if request.user.is_authenticated:
            if request.method == "POST":
                form = UpdateOtelOdaForm(request.POST, instance=ilgiliOda)
                if form.is_valid():
                    form.save()
                    return redirect("odadetay", odaID)
                else:
                    messages.error(request, "Hatalı Veri Girişi Olmuştur.")
        else:
            return redirect("anasayfa")
    # except Exception as a:
    except OtelOda.DoesNotExist:
        # Exceptionsların hatasını konsola basar
        # traceback.print_exc()
        return redirect("404")
    return render(request, "odadetay.html", context)


# Blokaj sayfası
@login_required(login_url="anasayfa")
def blokaj(request: HttpRequest) -> RedirectOrResponse:
    context = {}
    otel = OtelYonetim.objects.filter(owner=request.user).first()

    odalar = OtelOda.objects.filter(otel=otel).all()
    context["odalar"] = odalar
    ilgiliform = UpdateBlokaj()
    context["blokajForm"] = ilgiliform

    if request.method == "POST":
        form = UpdateBlokaj(request.POST)

        if form.is_valid():
            # Bellekte beklet
            form = form.save(commit=False)
            # Foreign Key'e atamasını yap
            form.otel = otel
            # Kaydet
            form.save()
            messages.success(request, "Blokaj Atanmıştır!")
            return redirect("blokaj")

    return render(request, "blokaj.html", context)


# Oda sil functions
@login_required(login_url="anasayfa")
def odasil(request: HttpRequest, odaID: int) -> HttpResponse:
    oda = OtelOda.objects.filter(id=odaID).first()

    if oda and request.user.is_authenticated:
        oda.delete()
        messages.success(request, f"{oda} Numaralı Oda Başarıyla Silindi")
        return redirect("dashboard")
    else:
        return redirect("404")


# Misafir Detay
@login_required(login_url="anasayfa")
def misafirdetay(request: HttpRequest, misafirID: int) -> HttpRequest:
    context = {}
    konuk = KonukBilgileri.objects.filter(id=misafirID).first()
    context["kisi"] = konuk
    girisCikis = KonukCheckInveCheckOut.objects.filter(konuk=konuk).first()
    context["cikisgiris"] = girisCikis
    musteriForm = UpdateMusteriDetay(instance=konuk)
    context["musteriform"] = musteriForm

    if request.user.is_authenticated:
        if request.method == "POST":
            form = UpdateMusteriDetay(request.POST, instance=konuk)
            if form.is_valid():
                form.save()
                messages.success(request, "Müşteriye not başarıyla eklendi!")
                return redirect("misafirdetay", misafirID)
    else:
        return redirect("anasayfa")

    return render(request, "misafirdetay.html", context)


@login_required(login_url="anasayfa")
def checkoutyaptir(request: HttpRequest, misafirID: int) -> HttpResponseRedirect:
    checkoutislemi = KonukCheckInveCheckOut.objects.filter(konuk__id=misafirID).first()
    # print("Kişi: ", checkoutislemi.oda.odaNumarasi)

    if checkoutislemi and request.user.is_authenticated:
        checkoutislemi.oda.odaBosMu = True
        checkoutislemi.delete()
        return redirect("dashboard")
    else:
        return redirect("404")


# Muhasebe
@login_required(login_url="anasayfa")
def muhasebe(request: HttpRequest) -> HttpRequest:
    return render(request, "muhasebe.html")


# Logout Sayfasıdır
@login_required(login_url="anasayfa")
def cikisYap(request: HttpRequest) -> HttpResponseRedirect:
    if request.user.is_authenticated:
        logout(request)
        return redirect("anasayfa")
    else:
        return redirect("404")


# 404 Sayfası
def hatasayfasi(request: HttpRequest) -> HttpResponse:
    return render(request, "404.html")
