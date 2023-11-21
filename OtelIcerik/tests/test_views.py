from django.test import TestCase, Client
from django.urls import reverse, resolve
from OtelIcerik.models import *
from django.utils import timezone
import json


class TestViews(TestCase):
    def setUp(self):
        # Setup Start
        # Test User (dipnot login_required decarator var!)
        self.usercreate = User.objects.create_user(
            username="test", password="testpassword"
        )
        self.user = User.objects.filter(username="test").first()
        # Otel Yönetim
        self.otelyonetimcreate = OtelYonetim.objects.create(
            owner=self.user,
            title="Otelcik",
            address="Adrescik Selam Sok. No 30",
            telephone="123123123",
        )
        self.otelyonetim = OtelYonetim.objects.filter(owner=self.user).first()
        # Oda
        self.oda = OtelOda.objects.create(
            otel=self.otelyonetim, odaNumarasi="303", odaTipi="KingSuit"
        )
        # Konuk
        self.konuk = KonukBilgileri.objects.create(
            otel=self.otelyonetim,
            firstname="Halil",
            lastname="Aksoy",
            birthday="22.10.1994",
            uyrugu="TC",
        )
        # Check In Out
        self.konukcheckincheckout = KonukCheckInveCheckOut.objects.create(
            otel=self.otelyonetim,
            konuk=self.konuk,
            oda=self.oda,
            checkIn=timezone.now(),
            checkOut=timezone.now(),
        )

        self.client = Client()
        self.anasayfa_url = reverse("anasayfa")
        self.muhasebe_url = reverse("muhasebe")
        self.odaekle_url = reverse("odaekle")
        self.dashboard_url = reverse("dashboard")
        self.checkout_yaptir_url = reverse(
            "misafircheckout", args=[self.konukcheckincheckout.id]
        )

        # Login Edelim (Login Required olduğundan dolayı)
        self.client.login(username="test", password="testpassword")
        # Setup End

    # Start Tests Points Here

    def test_anasayfa(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_muhasebe(self):
        response = self.client.get(self.muhasebe_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "muhasebe.html")

    def test_odaekle_post(self):
        post_data = {"room-tipi": "King Suit", "room-numarasi": "201"}

        # Post İsteği
        response = self.client.post(self.odaekle_url, post_data)

        # İstenilen Sayfaya Yönlendi mi?
        self.assertRedirects(response, self.dashboard_url)

        # Veritabanı sorgusu
        self.assertTrue(
            OtelOda.objects.filter(
                otel=self.otelyonetim, odaNumarasi="201", odaTipi="King Suit"
            ).exists()
        )

    def test_odaekle_post_data_missing(self):
        post_data = {
            "room-tipi": "Single Room",
        }

        # Post İsteği
        response = self.client.post(self.odaekle_url, post_data)

        # Yönlendirmeler Çalıştı mı?
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.dashboard_url)

    def test_odaekle_nonauth(self):
        response = self.client.get(self.odaekle_url)

        self.assertRedirects(response, self.dashboard_url)

    def test_checkoutyaptir_delete(self):
        response = self.client.get(self.checkout_yaptir_url)

        # Yönelendirme İşlemi
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.dashboard_url)

        # Silindikten sonra oda bilgisi güncelle
        self.oda.refresh_from_db()
        self.assertTrue(self.oda.odaBosMu)

        # Check-in/Check-Out kaydı silindimi ?
        with self.assertRaises(KonukCheckInveCheckOut.DoesNotExist):
            KonukCheckInveCheckOut.objects.get(pk=self.konukcheckincheckout.id)
