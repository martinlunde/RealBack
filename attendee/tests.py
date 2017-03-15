
from django.test import Client, TestCase
from django.urls import reverse

c = Client()


class WebsiteStabilityTestCase(TestCase):
    def test_frontpage_availability(self):
        self.assertEqual(c.get('/').status_code, 200)

    def test_about_us_availability(self):
        self.assertEqual(c.get(reverse('about')).status_code, 200)
