"""
Lecturer RESTful API functions
"""

from django.http import JsonResponse
from django.views import View
from lecturer import models as lecturer_models


def lecture_details(request, pin=None):
    """ Fetch lecture details from PIN """
    if pin is None:
        return JsonResponse({'success': False, 'message': 'Missing PIN'})

    try:
        lecture = lecturer_models.Lecture.objects.get(pin=pin)
    except lecturer_models.Lecture.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid PIN'})

    return JsonResponse({
        'success': True,
        'lecture_name': lecture.title,
    })


class LectureQuestions(View):
    def get(self, request, pin=None):
        pass

    def post(self, request, pin=None):
        pass


class LectureSpeed(View):
    def get(self, request, pin=None):
        pass

    def post(self, request, pin=None):
        pass
