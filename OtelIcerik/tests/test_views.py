from django.test import TestCase, Client
from django.urls import reverse
from OtelIcerik.models import *
from django.utils import timezone
from django.contrib.messages import get_messages


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
        self.misafir_ekle_url = reverse("misafirekle", args=[1])
        self.odadetay_url = reverse("odadetay", args=[1])
        self.checkout_yaptir_url = reverse(
            "misafircheckout", args=[self.konukcheckincheckout.id]
        )
        self.checkout_yaptir_invalid_id_url = reverse("misafircheckout", args=[21312731])
        self.error_url = reverse("404")

        # Login Edelim (Login Required olduğundan dolayı)
        self.client.login(username="test", password="testpassword")
        # Setup End

    # Start Tests Points Here

    def test_anasayfa(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, 200)

    def test_dashboard(self):
        response = self.client.get(self.dashboard_url)

        # Http Status 200
        self.assertEqual(response.status_code, 200)

        # Context içinde 'odalar' ve 'musteriler' key'leri olmalı
        self.assertIn("odalar", response.context)
        self.assertIn("musteriler", response.context)

        # 'odalar' ve 'musteriler' context değişkenleri, beklenen model örneklerini içermeli
        self.assertQuerysetEqual(response.context["odalar"], [self.oda])
        self.assertQuerysetEqual(
            response.context["musteriler"], [self.konukcheckincheckout]
        )

    def misafir_ekle_post_valid_data(self):
        post_data = {
            "first": "Coder",
            "last": "Mungan",
            "dogumtarihi": "22.10.1994",
            "uyruk": "TC",
            "tc": "11111111111",
            "passaport": "11111111111",
            "guest_note": "Kampus.us!",
            "price": 300.00,
            "parabirimi": "TRY",
            "checkin": timezone.now(),
            "checkout": timezone.now(),
        }

        # Post isteği oluşturuldu!
        response = self.client.post(self.misafir_ekle_url, post_data)

        # İstenilen sayfa durumu Redirect Status Kodu 302 olmalı
        self.assertEqual(response.status_code, 302)

        # Message modülü kontrolü
        storage = get_messages(response.wsgi_request)
        messages = [message.message for message in storage]
        self.assertIn("Müşteri başarıyla kaydedilmiştir!", messages)

        # Yönlenen url doğru mu?
        self.assertEqual(response.url, self.odadetay_url)

        # Müşteri ismi sayfada gözüküyor mu?
        response_odadetay = self.client.get(self.odadetay_url)
        self.assertContains(response_odadetay, 'Coder Mungan')

    def misafir_ekle_post_invalid_data(self):
        post_data = {
            "first": "Coder",
            "last": "Mungan",
            "dogumtarihi": "22.10.1994",
            "uyruk": "TC",
            "guest_note": "Kampus.us!",
            "price": 300.00,
            "parabirimi": "TRY",
            "checkin": timezone.now(),
            "checkout": timezone.now(),
        }

        # Post isteği oluşturuldu!
        response = self.client.post(self.misafir_ekle_url, post_data)

        # İstenilen sayfa durumu Redirect Status Kodu 302 olmalı
        self.assertEqual(response.status_code, 302)

        # Message modülü kontrolü
        storage = get_messages(response.wsgi_request)
        messages = [message.message for message in storage]
        self.assertIn("Lütfen Tc Kimliğini veya Passport ID'sini Giriniz!", messages)

        # Yönlenen url doğru mu?
        self.assertEqual(response.url, self.odadetay_url)


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

        # Mesaj İsteği Geldi Mi?
        oda = OtelOda.objects.filter(odaNumarasi="201").first()
        storage = get_messages(
            response.wsgi_request
        )  # Django'nun uygulama sunucusu (WSGI) tarafından işlenen bir HTTP isteğini temsil eden bir HttpRequest nesnesidir.
        messages = [message.message for message in storage]
        self.assertIn(
            f"Başarıyla {oda.odaNumarasi}'nolu odanız oluşturuldu!", messages
        )  # assertIn fonksiyonu, bir değerin belirli bir koleksiyon içinde bulunup bulunmadığını kontrol eder.

    def test_odaekle_post_data_missing(self):
        post_data = {
            "room-tipi": "Single Room",
        }
        # Post İsteği
        response = self.client.post(self.odaekle_url, post_data)

        # Yönlendirmeler Çalıştı mı?
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.dashboard_url)

        # Messages Çalıştı mı?
        storage = get_messages(response.wsgi_request)
        messages = [message.message for message in storage]
        self.assertIn("Boşlukları Lütfen Doldurunuz", messages)

    def test_odaekle_with_invalid_data(self):
        post_data = {
            "invalid-form-input": "Single-Room",
            "invalid-second-form-input": "306",
        }

        # Post İsteği
        response = self.client.post(self.odaekle_url, post_data)
        # Else Redirect(Dashboard)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.dashboard_url)

        # Messages Çalıştı mı?
        storage = get_messages(response.wsgi_request)
        messages = [message.message for message in storage]
        self.assertIn("Boşlukları Lütfen Doldurunuz", messages)

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
    
    def test_checkoutyaptir_invalid_id_delete(self):
        response = self.client.get(self.checkout_yaptir_invalid_id_url)

        # Yönelendirme İşlemi
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.error_url)

    def tearDown(self):
        self.client.logout()
        self.usercreate.delete()
        self.user.delete()
        self.otelyonetim.delete()
        self.otelyonetimcreate.delete()
        self.oda.delete()
        self.konuk.delete()
        self.konukcheckincheckout.delete()
