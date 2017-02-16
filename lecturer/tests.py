
from django.test import Client, TestCase


c = Client()


class WebsiteStabilityTestCase(TestCase):
    def test_availability(self):
        self.assertEqual(c.get('/lecturer/').status_code, 200)
