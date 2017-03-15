
from django.test import Client, TestCase
from django.contrib import auth
from realback_api import models
from django.contrib.auth import get_user_model


c = Client()


class WebsiteStabilityTestCase(TestCase):
    def test_availability(self):
        user = get_user_model().objects.create_user(
            username='test_user',
            email='test@user.com',
            password='testpass1234'
        )

        course = models.Course(user=user, title="TDT4100")
        course.save()
        lecture = models.Lecture(course=course, title="test_lecture")
        lecture.save()

        # Testing if user is redirected properly if trying to access login-restricted pages.
        self.assertEqual(c.get('/lecturer/').status_code, 302)
        # TODO test against api for courses and lectures

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

    # def test_lecturers_courses(self):
    #     user = auth.get_user_model().objects.create_user(
    #         username='test_user',
    #         email='test@user.com',
    #         password='testpass1234'
    #     )
    #     c.force_login(user=user)
    #
    #     course = models.Course(user=user, title="TDT4100")
    #     course.save()
    #
    #     # Check if the created course is shown on the lecturers page.
    #     self.assertEqual(c.get('/lecturer/TDT4100').status_code, 200)

    # def test_courses_lectures(self):
    #     user = auth.get_user_model().objects.create_user(
    #         username='test_user',
    #         email='test@user.com',
    #         password='testpass1234'
    #     )
    #     c.force_login(user=user)
    #
    #     course = models.Course(user=user, title="TDT4100")
    #     course.save()
    #     lecture = models.Lecture(course=course, title="test_lecture")
    #     lecture.save()
    #
    #     # Check if the created lecture is listed under its course, and is available to the lecturer.
    #     self.assertEqual(c.get('/lecturer/TDT4100/test_lecture').status_code, 200)
