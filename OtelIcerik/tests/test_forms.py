from django.test import TestCase, Client
from django.urls import reverse
from OtelIcerik.models import *
from django.utils import timezone
from django.contrib.messages import get_messages


class TestForm(TestCase):
    
    def setupTest(self):
        self.client = Client()
        pass