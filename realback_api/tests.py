
from django.test import Client, TestCase
from . import models
from django.contrib.auth import get_user_model
import json

c = Client()


class ApiTestCase(TestCase):
    """The different API tests will check if our api is returning proper json responses or returning correct
    error messages based on the situation. The comments below will therefore only be a pointer to if the test
    exists for testing pass or fail of a request."""

    """Testing course creation, deletion and update"""
    def testNewCourse(self):
        get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c.login(username='test@test.com', password='kNouYH8J3KjJH3')

        """Test if passing"""
        c.post('/courses/', {'title': 'TDT4140'})
        response = c.get('/courses/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

        """Test if failing"""
        response = c.post('/courses/', {'titleteas': 'TDT4140'})
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

    def testCourseDetailGet(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c.login(username='test@test.com', password='kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        course.save()

        """Test if passing"""
        response = c.get('/courses/' + str(course.id) + '/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

        """Test if failing"""
        response = c.get('/courses/' + str(500) + '/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

    def testCourseDetailPost(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c.login(username='test@test.com', password='kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        course.save()

        """Test if passing"""
        c.post('/courses/' + str(course.id) + '/', {'title': 'TDT4140'})
        response = c.get('/courses/' + str(course.id) + '/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

        """Test if failing"""
        response = c.post('/courses/' + str(course.id) + '/', {'nope': 'TDT4140'})
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

        """Test if failing"""
        response = c.post('/courses/' + str(500) + '/', {'title': 'TDT4140'})
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

    def testCourseDetailDelete(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c.login(username='test@test.com', password='kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4180")
        course.save()

        """Test if passing"""
        response = c.delete('/courses/' + str(course.id) + '/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

        """Test if failing"""
        response = c.delete('/courses/' + str(500) + '/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

    def testLectureDetail(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        course.save()
        lecture = models.Lecture(course=course, title="Lecture1")
        lecture.save()

        response = c.get('/lectures/' + lecture.pin + '/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

    def testLectureDetailFalse(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        course.save()
        lecture = models.Lecture(course=course, title="Lecture1")

        response = c.get('/lectures/' + lecture.pin + '/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

    """Testing CourseLecture creation and updates"""
    def testCourseLectureGet(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c.login(username='test@test.com', password='kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        course.save()

        """Test if passing"""
        response = c.get('/courses/' + str(course.id) + '/lectures/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

    def testCourseLecturePostCreation(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c.login(username='test@test.com', password='kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        course.save()

        """Test if passing"""
        response = c.post('/courses/' + str(course.id) + '/lectures/', {'title': 'lecture1'})
        decoded = json.loads(response.content)
        self.assertEqual(decoded['lecture']['lecture_title'], 'lecture1')

        """Test if failing"""
        response = c.post('/courses/' + str(500) + '/lectures/', {'title': 'lecture1'})
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

    def testLectureStats(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c.login(username='test@test.com', password='kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        course.save()
        lecture = models.Lecture(course=course, title="Lecture1")
        lecture.save()

        """Test if passing"""
        response = c.get('/courses/' + str(course.id) + '/stats/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

    def testLectureResetVolumeAndPace(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c.login(username='test@test.com', password='kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        course.save()
        lecture = models.Lecture(course=course, title="Lecture1")
        lecture.save()

        """Test if volume reset is passing"""
        response = c.get('/lectures/' + lecture.pin + '/reset/volume/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

        """Test if pace reset is passing"""
        response = c.get('/lectures/' + lecture.pin + '/reset/pace/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

    def testLectureVolumeGet(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c.login(username='test@test.com', password='kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        course.save()
        lecture = models.Lecture(course=course, title="Lecture1")
        lecture.save()

        """Test if passing"""
        response = c.get('/lectures/' + lecture.pin + '/volume/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

        """Test if failing"""
        response = c.get('/lectures/' + '7FSA6C' + '/volume/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

    def testLectureVolumePost(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c.login(username='test@test.com', password='kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        course.save()
        lecture = models.Lecture(course=course, title="Lecture1")
        lecture.save()

        """Test if passing"""
        response = c.post('/lectures/' + lecture.pin + '/volume/', {'volume': True})
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

    def testLectureRating(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c.login(username='test@test.com', password='kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        course.save()
        lecture = models.Lecture(course=course, title="Lecture1")
        lecture.save()

        """Test if passing"""
        response = c.post('/lectures/' + lecture.pin + '/rate/', {'rating': 4})
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

        """Test if failing"""
        response = c.post('/lectures/' + '714HSB' + '/rate/', {'rating': 4})
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

        """Test if passing"""
        response = c.get('/lectures/' + lecture.pin + '/reset_rating/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

        """Test if failing"""
        response = c.get('/lectures/' + '714HSB' + '/reset_rating/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

    def testLectureTimer(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c.login(username='test@test.com', password='kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        course.save()
        lecture = models.Lecture(course=course, title="Lecture1")
        lecture.save()

        """Test if passing"""
        response = c.get('/lectures/' + lecture.pin + '/timer/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

        """Test if failing"""
        response = c.get('/lectures/' + '714HSB' + '/timer/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

        """Test if passing"""
        response = c.get('/lectures/' + lecture.pin + '/start_timer/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

        """Test if failing"""
        response = c.get('/lectures/' + '714HSB' + '/start_timer/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

        """Test if passing"""
        response = c.get('/lectures/' + lecture.pin + '/stop_timer/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

        """Test if failing"""
        response = c.get('/lectures/' + '714HSB' + '/stop_timer/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

    def testLectureQuestions(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        c.login(username='test@test.com', password='kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4145")
        course.save()
        lecture = models.Lecture(course=course, title="Lecture1")
        lecture.save()
        question = models.Question(lecture=lecture, text="Why is the sky blue?")
        question.save()

        response = c.get('/lectures/' + lecture.pin + '/questions/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

        response = c.post('/lectures/' + lecture.pin + '/questions/', {'text': 'what is this?'})
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)

        response = c.post('/lectures/' + '714HSB' + '/questions/', {'text': 'what is this?'})
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], False)

        """Questions votes"""
        response = c.post('/lectures/' + lecture.pin + '/questions/' + str(question.id) + '/vote/')
        decoded = json.loads(response.content)
        self.assertEqual(decoded['success'], True)


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
        test_lecture = models.Lecture(course=test_course, title="Lecture1", pin=pin)
        test_lecture.save()

        # Test if lectures and courses are created correctly, and if the relevant functions are
        # working as intended.
        self.assertEqual(test_course.title, "TDT4140")
        self.assertEqual(test_lecture.title, "Lecture1")
        self.assertEqual(test_lecture.course, test_course)
        # test_lecture.reset_pace()
        # test_lecture.reset_volume()
        # self.assertEqual(test_lecture.pace, 0)
        # self.assertEqual(test_lecture.volume, 0)

    def test_questions(self):
        user = get_user_model().objects.create_user('test_user', 'test@test.com', 'kNouYH8J3KjJH3')
        course = models.Course(user=user, title="TDT4140")
        course.save()
        lecture = models.Lecture(course=course, title="Lecture1", pin=models._generate_pin())
        lecture.save()

        test_questions = models.Question(lecture=lecture, text="Why is the sky blue?")
        test_questions.save()

        # Test if questions attributes are functioning as intended.
        self.assertEqual(test_questions.lecture, lecture)
        self.assertEqual(test_questions.text, "Why is the sky blue?")
        self.assertEqual(test_questions.votes, 0)
