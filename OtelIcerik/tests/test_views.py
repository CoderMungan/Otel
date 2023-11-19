from django.test import TestCase, Client
from django.urls import reverse, resolve
from OtelIcerik.models import *
import json


class TestViews(TestCase):
    

    def setUp(self):
        self.client = Client()
        self.muhasebe_url = reverse('muhasebe')

        # Test User (dipnot login_required decarator var!)
        self.user = User.objects.create_user(username='test', password='testpassword')
        self.client.login(username = 'test', password = 'testpassword')

    def test_muhasebe(self):

        response = self.client.get(self.muhasebe_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'muhasebe.html')