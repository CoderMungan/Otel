from django.test import SimpleTestCase , Client
from django.urls import reverse, resolve
from OtelIcerik.views import *
from OtelRestApiBlokaj.views import *

class TestUrls(SimpleTestCase):

    def setUp(self):
        self.client = Client()
        self.anasayfa_url = reverse('anasayfa')
        self.dashboard_url = reverse('dashboard')
        self.blokaj_url = reverse('blokaj')
        self.api_url = reverse('apitest')
        self.checkstatus_url = reverse('checkstatus')
        self.misafdetay_url = reverse('misafirdetay', args=[1])
        self.misafirekle_url = reverse('misafirekle', args=[1])
        self.misafircheckout_url = reverse('misafircheckout', args=[1])
        self.muhasebe_url = reverse('muhasebe')
        self.odadetay_url = reverse('odadetay', args=[1])
        self.odasil_url = reverse('odasil', args=[1])
        self.odaekle_url = reverse('odaekle')
        self.logout_url = reverse('logout')





    def test_home_url(self):
        response = self.client.get(self.anasayfa_url)

        # Check the Status Codes
        self.assertEqual(response.status_code, 200)
        # Functions match
        self.assertEqual(resolve(self.anasayfa_url).func, anasayfa)


    def test_dashboard_url(self):
        print("gelen paramlar:", resolve(self.dashboard_url))
        # Functions match
        self.assertEqual(resolve(self.dashboard_url).func, dashboard)


    def test_api_url(self):

        # Functions match
        self.assertEqual(resolve(self.api_url).func, send_routes)

    def test_api_checkstatus_url(self):

        # Functions match
        self.assertEqual(resolve(self.checkstatus_url).func, checkstatus)

    def test_misafirdetay_url(self):

        # Functions match
        self.assertEqual(resolve(self.misafdetay_url).func, misafirdetay)

    def test_misafir_ekle_url(self):

        # Functions match
        self.assertEqual(resolve(self.misafirekle_url).func, misafirekle)
    
    def test_misafir_checkout_url(self):

        # Functions match
        self.assertEqual(resolve(self.misafircheckout_url).func, checkoutyaptir)

    def test_blokaj_url(self):

        # Functions match
        self.assertEqual(resolve(self.blokaj_url).func, blokaj)

    def test_muhasebe_url(self):

        # Functions match
        self.assertEqual(resolve(self.muhasebe_url).func, muhasebe)

    def test_odadetay_url(self):

        # Functions match
        self.assertEqual(resolve(self.odadetay_url).func, odadetay)

    def test_odasil_url(self):

        # Functions match
        self.assertEqual(resolve(self.odasil_url).func, odasil)

    def test_odaekle_url(self):

        #Functions match
        self.assertEqual(resolve(self.odaekle_url).func, odaEkle)

    def test_logout_url(self):

        #Functions match
        self.assertEqual(resolve(self.logout_url).func, cikisYap)