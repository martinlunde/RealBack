
from django.test import Client, TestCase
from django.contrib import auth


c = Client()


class WebsiteStabilityTestCase(TestCase):
    def test_availability(self):
        self.assertEqual(c.get('/lecturer/').status_code, 302)  # We are getting redirect when not logged in, so 302

    def test_lecturer_login(self):
        user = auth.get_user_model().objects.create_user(
            username='test_user',
            email='test@user.com',
            password='testpass1234'
        )
        c.force_login(user=user)
        logged_in_user = auth.get_user(c)
        # Check that user is authenticated
        self.assertTrue(logged_in_user.is_authenticated)
        # Check that we are not redirected anymore
        self.assertEqual(c.get('/lecturer/').status_code, 200)
