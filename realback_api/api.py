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
            return JsonResponse({'success': False, 'message': 'Missing lecture PIN'})

        try:
            lecture = models.Lecture.objects.get(pin=pin)
        except models.Lecture.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Lecture does not exist'})

        return JsonResponse({
            'success': True,
            'lecture': lecture.as_dict(),
        })

    @method_decorator(login_required)
    def post(self, request, pin=None):
        """ Update details for existing lecture """
        form = forms.LectureForm(request.POST)
        if form.is_valid():
            try:
                lecture = models.Lecture.objects.get(pin=pin, course__user=request.user)
            except models.Lecture.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Lecture with PIN does not exist for this user'})

            lecture.title = form.cleaned_data['title']
            lecture.save()
            return JsonResponse({
                'success': True,
                'lecture': lecture.as_dict(),
            })

        return JsonResponse({
            'success': False,
            'errors': form.errors,
        })


class LectureQuestions(View):
    def get(self, request, pin=None):
        """ Read list of latest questions """
        question_list = models.Question.objects.filter(lecture__pin=pin).order_by('-votes', '-timestamp')
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
            }, status=201)

        return JsonResponse({
            'success': False,
            'errors': form.errors,
        })


class LectureQuestionVotes(View):
    def post(self, request, pin=None, question_id=None):
        """ Create vote on question """
        if question_id is None or pin is None:
            return JsonResponse({'success': False, 'message': 'Missing question ID or lecture PIN'})

        try:
            question = models.Question.objects.get(id=question_id, lecture__pin=pin)
        except models.Lecture.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Question ID does not exist for this lecture'})

        question.votes += 1
        question.save()
        return JsonResponse({
            'success': True,
            'question': question.as_dict(),
        })


class LecturePace(View):
    def get(self, request, pin=None):
        """ Read digest of lecture pace opinions """
        if pin is None:
            return JsonResponse({'success': False, 'message': 'Missing lecture PIN'})

        try:
            lecture = models.Lecture.objects.get(pin=pin)
        except models.Lecture.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Lecture does not exist'})

        return JsonResponse({
            'success': True,
            'lecture_pace': lecture.pace,
        })

    def post(self, request, pin=None):
        """ Create opinion on lecture pace """
        if pin is None:
            return JsonResponse({'success': False, 'message': 'Missing lecture PIN'})

        form = forms.PaceForm(request.POST)
        if form.is_valid():
            try:
                lecture = models.Lecture.objects.get(pin=pin)
            except models.Lecture.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Lecture does not exist'})

            pace = form.cleaned_data['pace']
            if pace:
                lecture.pace += 1
            else:
                lecture.pace -= 1
            lecture.save()

            return JsonResponse({
                'success': True,
                'lecture': lecture.as_dict(),
            })

        return JsonResponse({
            'success': False,
            'errors': form.errors,
        })


class LectureVolume(View):
    def get(self, request, pin=None):
        """ Read digest of lecture volume opinions """
        if pin is None:
            return JsonResponse({'success': False, 'message': 'Missing lecture PIN'})

        try:
            lecture = models.Lecture.objects.get(pin=pin)
        except models.Lecture.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Lecture does not exist'})

        return JsonResponse({
            'success': True,
            'lecture_pace': lecture.volume,
        })

    def post(self, request, pin=None):
        """ Create opinion on lecture volume """
        if pin is None:
            return JsonResponse({'success': False, 'message': 'Missing lecture PIN'})

        form = forms.VolumeForm(request.POST)
        if form.is_valid():
            try:
                lecture = models.Lecture.objects.get(pin=pin)
            except models.Lecture.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Lecture does not exist'})

            volume = form.cleaned_data['volume']
            if volume:
                lecture.volume += 1
            else:
                lecture.volume -= 1
            lecture.save()

            return JsonResponse({
                'success': True,
                'lecture': lecture.as_dict(),
            })

        return JsonResponse({
            'success': False,
            'errors': form.errors,
        })


class Courses(View):
    @method_decorator(login_required)
    def get(self, request):
        """ Read list of latest courses for user """
        course_list = models.Course.objects.filter(user=request.user).order_by('-id')
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
                    'message': "Course with this title already exists"
                })

            course = form.save(commit=False)
            course.user = request.user
            course.save()
            return JsonResponse({
                'success': True,
                'Course': course.as_dict()
            }, status=201)

        return JsonResponse({
            'success': False,
            'errors': form.errors,
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
        try:
            course = models.Course.objects.get(id=course_id)
        except models.Course.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Course ID does not exist'})

        if course.user != request.user:
            return JsonResponse({'success': False, 'message': 'Access denied'})

        lecture_count = models.Lecture.objects.count(course__id=course_id, course__user=request.user)
        lecture = models.Lecture(
            course=course,
            title=str(request.user) + "_" + str(course.title) + "_" + str(lecture_count + 1)
        )
        lecture.save()
        return JsonResponse({
            'success': True,
            'lecture': lecture.as_dict(),
        }, status=201)
