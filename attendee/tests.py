
from django.test import Client, TestCase
from attendee import models


c = Client()


class WebsiteStabilityTestCase(TestCase):
    def test_availability(self):
        self.assertEqual(c.get('/').status_code, 200)


class ModelTestCase(TestCase):
    def test_generate_pin(self):
        """ Test if attendee login pin is generated """
        # TODO test more properties? character set, all uppercase
        self.assertEqual(len(models.generate_pin()), 6)
