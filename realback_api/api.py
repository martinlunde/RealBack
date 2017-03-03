"""
RealBack RESTful API functions
"""

from django.http import JsonResponse
from django.views import View
from . import models


class LectureDetails(View):
    def get(self, request, pin=None):
        """ Fetch lecture details from PIN """
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
        pass


class LectureQuestions(View):
    def get(self, request, pin=None):
        """ Get list of latest questions """
        pass

    def post(self, request, pin=None):
        """ Post new question """
        pass


class LectureSpeed(View):
    def get(self, request, pin=None):
        """ Get digest of lecture speed opinions """
        pass

    def post(self, request, pin=None):
        """ Post opinion on lecture speed """
        pass
