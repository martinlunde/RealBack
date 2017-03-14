
from django.test import TestCase
from . import models
from django.contrib.auth import get_user_model


class ModelTestCase(TestCase):
    def test_generate_pin(self):
        """ Test if attendee login pin is generated """
        pin = models._generate_pin()
        charset = "ABCDEFGHIJKLMNPQRSTUVWXYZ123456789"

        # Test if pin has a length of 6 and is uppercase
        self.assertEqual(len(pin), 6)
        self.assertEqual(pin, pin.upper())

        # Test if pin i generated with the give charset
        for i in pin:
            self.assertEqual(i, charset[charset.rfind(i)])

    def test_return_course(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4180")

        # Testing if course returns a proper string
        self.assertEqual(str(course), course.title)

        # Testing if course returns a proper json/dictionary
        course_values = course.as_dict()
        self.assertEqual(course_values['course_title'], course.title)
        self.assertEqual(course_values['course_id'], course.id)

    def test_return_lecture(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        lecture = models.Lecture(course=course, title="Lecture1")

        # Testing if lecture returns a proper string
        self.assertEqual(str(lecture), lecture.title)

        # Testing if lecture returns a proper json/dictionary
        lecture_values = lecture.as_dict()
        self.assertEqual(lecture_values['lecture_pin'], lecture.pin)
        self.assertEqual(lecture_values['lecture_title'], lecture.title)
        self.assertEqual(lecture_values['lecture_start_time'], lecture.start_datetime)

    def test_return_question(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4110")
        lecture = models.Lecture(course=course, title="questionnaire")
        question = models.Question(lecture=lecture, text="Why is a rose red?")

        # Testing if question returns a proper json/dictionary
        question_values = question.as_dict()
        self.assertEqual(question_values['question_text'], question.text)
        self.assertEqual(question_values['question_votes'], question.votes)

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

    def test_lecture_and_course_creation(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        test_course = models.Course(user=user, title="TDT4140")
        test_course.save()

        pin = models._generate_pin()
        test_lecture = models.Lecture(course=test_course, title="Lecture1", pin=pin, pace=5)
        test_lecture.save()

        self.assertEqual(test_course.title, "TDT4140")
        self.assertEqual(test_lecture.title, "Lecture1")
        self.assertEqual(test_lecture.course, test_course)
        test_lecture.reset_pace()
        self.assertEqual(test_lecture.pace, 0)

    def test_questions(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4140")
        course.save()
        lecture = models.Lecture(course=course, title="Lecture1", pin=models._generate_pin())
        lecture.save()

        test_questions = models.Question(lecture=lecture, text="Why is the sky blue?")
        test_questions.save()

        self.assertEqual(test_questions.lecture, lecture)
        self.assertEqual(test_questions.text, "Why is the sky blue?")
        self.assertEqual(test_questions.votes, 0)
