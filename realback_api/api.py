"""
RealBack RESTful API functions
"""

from django.http import JsonResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from . import models


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
            'lecture_name': lecture.title,
        })

    @method_decorator(login_required)
    def put(self, request, pin=None):
        """ Update details for existing lecture """
        # TODO remember to check if user has access (owner) to lecture
        pass


class LectureQuestions(View):
    def get(self, request, pin=None):
        """ Read list of latest questions """
        pass

    def post(self, request, pin=None):
        """ Create new question """
        pass


class LectureSpeed(View):
    def get(self, request, pin=None):
        """ Read digest of lecture speed opinions """
        pass

    def post(self, request, pin=None):
        """ Create opinion on lecture speed """
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
        pass


class CourseDetails(View):
    @method_decorator(login_required)
    def get(self, request, course_id):
        """ Read course details for course_id """
        # TODO remember to check if user has access (owner) to course
        pass

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
