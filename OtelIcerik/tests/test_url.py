from django.test import SimpleTestCase
from django.urls import reverse, resolve
from OtelIcerik.views import *
from OtelRestApiBlokaj.views import *

class TestUrls(SimpleTestCase):

    def test_home_url(self):
        url = reverse('anasayfa')

        # Functions match
        self.assertEqual(resolve(url).func, anasayfa)

    def test_dashboard_url(self):
        url = reverse('dashboard')

        # Functions match
        self.assertEqual(resolve(url).func,dashboard)

    def test_api_url(self):
        url = reverse("apitest")

        # Functions match
        self.assertEqual(resolve(url).func, send_routes)

    def test_api_checkstatus_url(self):
        url = reverse("checkstatus")

        # Functions match
        self.assertEqual(resolve(url).func, checkstatus)


    def test_misafirdetay_url(self):
        url = reverse('misafirdetay', args=[1])

        # Functions match
        self.assertEqual(resolve(url).func, misafirdetay)

    def test_misafir_ekle_url(self):
        url = reverse('misafirekle', args=[1])

        # Functions match
        self.assertEqual(resolve(url).func, misafirekle)
    
    def test_misafir_checkout_url(self):
        url = reverse('misafircheckout', args=[1])

        # Functions match
        self.assertEqual(resolve(url).func, checkoutyaptir)

    def test_blokaj_url(self):
        url = reverse('blokaj')

        # Functions match
        self.assertEqual(resolve(url).func, blokaj)

    def test_muhasebe_url(self):
        url = reverse('muhasebe')

        # Functions match
        self.assertEqual(resolve(url).func, muhasebe)

    def test_odadetay_url(self):
        url = reverse('odadetay', args=[1])

        # Functions match
        self.assertEqual(resolve(url).func, odadetay)

    def test_odasil_url(self):
        url = reverse('odasil', args=[1])

        # Functions match
        self.assertEqual(resolve(url).func, odasil)

    def test_odaekle_url(self):
        url = reverse('odaekle')

        #Functions match
        self.assertEqual(resolve(url).func, odaEkle)

    def test_logout_url(self):
        url = reverse('logout')

        #Functions match
        self.assertEqual(resolve(url).func, cikisYap)