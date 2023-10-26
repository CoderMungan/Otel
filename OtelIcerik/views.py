from django.shortcuts import render,redirect

# Müsti Abi
import traceback


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

    oda = OtelOda.objects.all()
    context['odalar'] = oda


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
def odadetay(request,odaID):

    context = {}

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

    except OtelOda.DoesNotExist:
        # Exceptionsların hatasını konsola basar
        # traceback.print_exc()
        return redirect('404')

    return render(request, "odadetay.html",context)


# Blokaj sayfası
@login_required(login_url='anasayfa')
def blokaj(request):
    return render(request,'blokaj.html')


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