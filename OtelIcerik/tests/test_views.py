from django.test import TestCase, Client
from django.urls import reverse, resolve
from OtelIcerik.models import *
import json


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.anasayfa_url = reverse("anasayfa")
        self.muhasebe_url = reverse("muhasebe")
        self.odaekle_url = reverse("odaekle")
        self.dashboard_url = reverse("dashboard")

        # Test User (dipnot login_required decarator var!)
        self.usercreate = User.objects.create_user(
            username="test", password="testpassword"
        )
        self.user = User.objects.filter(username="test").first()
        self.client.login(username="test", password="testpassword")

        # Otel Yönetim
        self.otelyonetimcreate = OtelYonetim.objects.create(
            owner=self.user,
            title="Otelcik",
            address="Adrescik Selam Sok. No 30",
            telephone="123123123",
        )
        self.otelyonetim = OtelYonetim.objects.filter(owner=self.user).first()

    def test_anasayfa(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_muhasebe(self):
        response = self.client.get(self.muhasebe_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "muhasebe.html")

    def test_odaekle_post(self):

        post_data = {
            'otel' : self.otelyonetim,
            'room-tipi' : 'King Suit',
            'room-numarasi' : '201'
        }

        #Post İsteği
        response = self.client.post(self.odaekle_url, post_data)
        
        #İstenilen Sayfaya Yönlendi mi?
        self.assertRedirects(response, self.dashboard_url)

        #Veritabanı sorgusu
        self.assertTrue(OtelOda.objects.filter(otel = self.otelyonetim, odaNumarasi = '201', odaTipi = 'King Suit').exists())

    def test_odaekle_nonauth(self):

        response = self.client.get(self.odaekle_url)

        self.assertRedirects(response, self.dashboard_url)



