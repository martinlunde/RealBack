
from django.test import TestCase
from . import models
from django.contrib.auth import get_user_model


class ModelTestCase(TestCase):
    def test_generate_pin(self):
        """ Test if attendee login pin is generated """
        pin = models._generate_pin()
        self.assertEqual(len(pin), 6)
        # TODO test more properties? character set, all uppercase

    def test_lecture_save(self):
        """ Test if Lecture saves correctly to db """
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c1 = models.Course(user=user)
        c1.save()
        l1 = models.Lecture(course=c1)
        l1.save()
        title = 'Test1'
        l2 = models.Lecture(course=c1,
                            title=title,
                            pin=l1.pin)
        l2.save()
        self.assertNotEqual(l2.pin, l1.pin)
        self.assertEqual(l2.title, title)