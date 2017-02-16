
from django.test import Client, TestCase
from attendee import models


c = Client()


class WebsiteStabilityTestCase(TestCase):
    def test_availability(self):
        self.assertEqual(c.get('/').status_code, 200)


class ModelTestCase(TestCase):
    def test_generate_pin(self):
        """ Test if attendee login pin is generated """
        pin = models._generate_pin()
        self.assertEqual(len(pin), 6)
        # TODO test more properties? character set, all uppercase

    def test_lecture_save(self):
        """ Test if Lecture saves correctly to db """
        c1 = models.Course()
        c1.save()
        l1 = models.Lecture(course=c1)
        l1.save()
        title = 'Test1'
        description = 'Test description 1'
        l2 = models.Lecture(course=c1,
                            title=title,
                            description=description,
                            pin=l1.pin)
        l2.save()
        self.assertNotEqual(l2.pin, l1.pin)
        self.assertEqual(l2.title, title)
        self.assertEqual(l2.description, description)
