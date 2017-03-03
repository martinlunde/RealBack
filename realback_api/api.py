"""
RealBack RESTful API functions
"""

from django.http import JsonResponse
from django.views import View
from . import models

# TODO login required for applicable methods


class Lecture(View):
    def post(self, request):
        """ Create new lecture for course_id """
        # TODO receive course id in form
        # TODO remember to check if user has access (owner) to course
        pass


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


class Course(View):
    def get(self, request):
        """ Read list of latest courses for user """
        pass

    def post(self, request):
        """ Create new course for user """
        pass


class CourseDetails(View):
    def get(self, request, course_id):
        """ Read course details for course_id """
        # TODO remember to check if user has access (owner) to course
        pass

    def put(self, request, course_id):
        """ Update course details for course_id """
        # TODO remember to check if user has access (owner) to course
        pass
