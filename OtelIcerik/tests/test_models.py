from django.test import TestCase, Client
from OtelIcerik.models import *
from datetime import datetime, timedelta


class TestModel(TestCase):  # Unutmayın ki bu sınıf django.test.TestCase'den türetilmeli
    def setUp(self):
        # Otel sahibi (owner) oluştur
        self.owner = User.objects.create_user(
            username="otel_sahibi", password="parola123"
        )

        # Otel bilgileri oluştur
        self.otel = OtelYonetim.objects.create(
            owner=self.owner,
            title="Test Otel",
            address="Test Adres",
            telephone="1234567890",
        )

        # Oda bilgileri oluştur
        self.oda = OtelOda.objects.create(
            otel=self.otel,
            odaNumarasi="101",
            odaTipi="Standart Oda",
            odaTemizMi=True,
            odaArizaliMi=False,
            odaRezerveMi=False,
            odaBosMu=True,
        )

        # Konuk bilgileri oluştur
        self.konuk = KonukBilgileri.objects.create(
            otel=self.otel,
            firstname="John",
            lastname="Doe",
            birthday="1990-01-01",
            uyrugu="USA",
            musteriTC="12345678901",
            musteriID="ABC123",
            musteriNotu="Test notu",
            fiyat=200.00,
            kur="USD",
        )

        # Check-in ve Check-out işlemi oluştur
        self.checkin_checkout = KonukCheckInveCheckOut.objects.create(
            otel=self.otel,
            konuk=self.konuk,
            oda=self.oda,
            checkIn=datetime.now(),
            checkOut=datetime.now() + timedelta(days=1),
            color="#00FF00",
        )

    def tearDown(self):
        self.owner.delete()
        self.otel.delete()
        self.oda.delete()
        self.konuk.delete()
        self.checkin_checkout.delete()

    def test_otel_str(self):
        self.assertEqual(str(self.otel), "Test Otel")

    def test_oda_str(self):
        self.assertEqual(str(self.oda), "101")

    def test_konuk_str(self):
        self.assertEqual(str(self.konuk), "John Doe")

    def test_checkin_checkout_str(self):
        self.assertEqual(str(self.checkin_checkout), "John Doe")