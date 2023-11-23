from django.test import TestCase
from django.utils import timezone
from OtelIcerik.forms import UpdateOtelOdaForm, UpdateMusteriDetay, UpdateBlokaj
from OtelIcerik.models import *


class TestForms(TestCase):
    def setUp(self):
        self.usercreate = User.objects.create_user(
            username="test", password="testpassword"
        )
        # Otel Yönetim
        self.otelyonetimcreate = OtelYonetim.objects.create(
            owner=self.usercreate,
            title="Otelcik",
            address="Adrescik Selam Sok. No 30",
            telephone="123123123",
        )
 
        self.odacreate = OtelOda.objects.create(
            otel=self.otelyonetimcreate, odaNumarasi="303", odaTipi="KingSuit"
        )

        # Konuk
        self.konukcreate = KonukBilgileri.objects.create(
            otel=self.otelyonetimcreate,
            firstname="Halil",
            lastname="Aksoy",
            birthday="22.10.1994",
            uyrugu="TC",
        )
        self.konukcheckinandcheckout = KonukCheckInveCheckOut.objects.create(
            otel=self.otelyonetimcreate,
            konuk=self.konukcreate,
            oda=self.odacreate,
            checkIn=timezone.now(),
            checkOut=timezone.now(),
        )

    def test_update_otel_oda_form(self):
        form_data = {
            "odaNumarasi": "101",
            "odaTipi": "Standart",
            "odaTemizMi": True,
            "odaArizaliMi": False,
            "odaBosMu": False,
            "odaProblemi": "Sorun Yok",
        }
        form = UpdateOtelOdaForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_musteri_detay_form(self):
        form_data = {
            "musteriNotu": "Misafir için bir not.",
        }
        form = UpdateMusteriDetay(data=form_data)
        self.assertTrue(form.is_valid())

    def test_update_blokaj_form(self):
        form_data = {
            "konuk": self.konukcreate,
            "oda": self.odacreate,
            "checkIn": timezone.now(),
            "checkOut": timezone.now() + timezone.timedelta(days=2),
            "color": "#3d85c6",  # varsayılan renk seçeneği olduğunu varsayalım
        }
        form = UpdateBlokaj(data=form_data)
        self.assertTrue(form.is_valid())

    def tearDown(self):
        self.usercreate.delete()
        self.otelyonetimcreate.delete()
        self.konukcreate.delete()
        self.odacreate.delete()
        self.konukcheckinandcheckout.delete()