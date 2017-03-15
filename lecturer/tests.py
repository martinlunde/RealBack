
from django.test import Client, TestCase
from django.contrib.auth import get_user_model

c = Client()


class WebsiteStabilityTestCase(TestCase):
    def test_availability(self):
        self.assertEqual(c.get('/lecturer/').status_code, 302)  # We are getting redirect when not logged in, so 302
        # TODO maybe check for something more reliable than 302?

    def test_lecturer_login(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        user.save()

        # Test if lecturer is logged in upon login-request
        self.assertEqual(c.post('/login/', {'username': 'test_user', 'password': 'kNouYH8J3KjJH3'}).status_code, 200)