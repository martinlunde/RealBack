from django.test import Client, TestCase


c = Client()
response = c.get('/')
print(response.status_code)


class WebsiteStabilityTestCase(TestCase):
    def test_availability(self):
        self.assertEqual(c.get('/').status_code, 200)
