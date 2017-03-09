"""
RealBack RESTful API functions
"""

from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . import models, forms


class LectureDetails(View):
    def get(self, request, pin=None):
        """ Read lecture details from PIN """
        if pin is None:
            return JsonResponse({'success': False, 'message': 'Missing PIN'})

        try:
            lecture = models.Lecture.objects.get(pin=pin)
        except models.Lecture.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid PIN'})

        return JsonResponse({
            'success': True,
            'lecture': lecture.as_dict(),
        })

    @method_decorator(login_required)
    def put(self, request, pin=None):
        """ Update details for existing lecture """
        # TODO remember to check if user has access (owner) to lecture
        pass


class LectureQuestions(View):
    def get(self, request, pin=None):
        """ Read list of latest questions """
        question_list = models.Question.objects.filter(lecture__pin=pin)
        return JsonResponse({
            'success': True,
            'questions': [question.as_dict() for question in question_list],
        })

    def post(self, request, pin=None):
        """ Create new question """
        form = forms.QuestionForm(request.POST)
        if form.is_valid():
            lecture = models.Lecture.objects.get(pin=pin)
            question = form.save(commit=False)
            question.lecture = lecture
            question.save()
            return JsonResponse({
                'success': True,
                'question': question.as_dict(),
            })

        return JsonResponse({
            'success': False,
            'question_text': form.cleaned_data['text'],
        })


class LectureSpeed(View):
    def get(self, request, pin=None):
        if pin is None:
            return JsonResponse({'success': False, 'message': 'Missing PIN'})

        try:
            lecture = models.Lecture.objects.get(pin=pin)
        except models.Lecture.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid PIN'})

        return JsonResponse({
            'success': True,
            'speed': lecture.speed
        })

    def post(self, request, pin=None, faster=None):
        """ Create opinion on lecture speed """
        if pin is None:
            return JsonResponse({'success': False, 'message': 'Missing PIN'})
        if faster is None:
            return JsonResponse({'success': False, 'message': 'Missing bool value'})

        try:
            lecture = models.Lecture.objects.get(pin=pin)
        except models.Lecture.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid PIN'})

        if faster:
            lecture.speed += 1
        else:
            lecture.speed -= 1
        lecture.update()

        return JsonResponse({
            'success': True,
            'message': 'Lecture speed updated'
        })
        pass


class Courses(View):
    @method_decorator(login_required)
    def get(self, request):
        """ Read list of latest courses for user """
        course_list = models.Course.objects.filter(user=request.user)
        return JsonResponse({
            'success': True,
            'courses': [course.as_dict() for course in course_list],
        })

    @method_decorator(login_required)
    def post(self, request):
        """ Create new course for user """
        form = forms.CourseForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if models.Course.objects.filter(title=title, user=request.user).exists():
                return JsonResponse({
                    'success': False,
                    'message': "Course already exists"
                })

            c = models.Course(title=title, user=request.user).save()
            return JsonResponse({
                'success': True,
                'Course': c.as_dict()
            })


class CourseDetails(View):
    @method_decorator(login_required)
    def get(self, request, course_id):
        """ Read course details for course_id """
        # TODO remember to check if user has access (owner) to course
        course = models.Course.objects.get(id=course_id)
        if course.user != request.user:
            return JsonResponse({
                'success': False,
                'message': 'Access denied',
            })

        return JsonResponse({
            'success': True,
            'course': course.as_dict(),
        })

    @method_decorator(login_required)
    def put(self, request, course_id):
        """ Update course details for course_id """
        # TODO remember to check if user has access (owner) to course
        pass


class CourseLectures(View):
    @method_decorator(login_required)
    def get(self, request, course_id):
        """ Read list of latest lectures for course_id """
        # TODO remember to check if user has access (owner) to course
        lecture_list = models.Lecture.objects.filter(course__id=course_id, course__user=request.user)
        return JsonResponse({
            'success': True,
            'lectures': [lecture.as_dict() for lecture in lecture_list],
        })

    @method_decorator(login_required)
    def post(self, request, course_id):
        """ Create new lecture for course_id """
        # TODO remember to check if user has access (owner) to course
        course = models.Course.objects.get(id=course_id)
        if course.user != request.user:
            return JsonResponse({
                'success': False,
                'message': 'Access denied',
            })

        lecture_count = models.Lecture.objects.count(course__id=course_id, course__user=request.user)
        lecture = models.Lecture(
            course=course,
            title=str(request.user) + "_" + str(course.title) + "_" + str(lecture_count + 1)
        )
        lecture.save()
        response = JsonResponse({
            'success': True,
            'lecture': lecture.as_dict(),
        })
        # TODO set created status code
        return response
