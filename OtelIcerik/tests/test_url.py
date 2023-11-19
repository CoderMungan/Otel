from django.test import SimpleTestCase
from django.urls import reverse, resolve
from OtelIcerik.views import *


class TestUrls(SimpleTestCase):

    def test_home_url(self):
        url = reverse('anasayfa')
        print(resolve(url))
        # Functions match
        self.assertEqual(resolve(url).func, anasayfa)


    def test_misafirdetay_url(self):
        url = reverse('misafirdetay', args=[1])
        print(resolve(url))
        # Functions match
        self.assertEqual(resolve(url).func, misafirdetay)