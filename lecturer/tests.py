
from django.test import Client, TestCase


c = Client()


class WebsiteStabilityTestCase(TestCase):
    def test_availability(self):
        self.assertEqual(c.get('/lecturer/').status_code, 302)  # We are getting redirect when not logged in, so 302
        # TODO maybe check for something more reliable than 302?
