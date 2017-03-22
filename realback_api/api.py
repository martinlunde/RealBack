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
        try:
            lecture = models.Lecture.objects.get(pin=pin)
        except models.Lecture.DoesNotExist:
            return JsonResponse({
                'success': False,
                'errors': {
                    'message': ['Lecture does not exist'],
                },
            })

        lecture.attendee_counter += 1
        lecture.save()
        return JsonResponse({
            'success': True,
            'lecture': lecture.as_dict(),
        })

    @method_decorator(login_required)
    def post(self, request, pin=None):
        """ Update details for existing lecture """
        # TODO remember to check if user has access (owner) to lecture
        form = forms.LectureForm(request.POST)
        if form.is_valid():
            try:
                lecture = models.Lecture.objects.get(pin=pin, course__user=request.user)
            except models.Lecture.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'errors': {
                        'message': ['Lecture with PIN does not exist for this user'],
                    },
                })

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

    @method_decorator(login_required)
    def delete(self, request, pin=None):
        """ Delete lecture with pin """
        # TODO remember to check if user has access (owner) to lecture
        try:
            lecture = models.Lecture.objects.get(pin=pin, course__user=request.user)
        except models.Lecture.DoesNotExist:
            return JsonResponse({
                'success': False,
                'errors': {
                    'message': ['Lecture with PIN does not exist for this user'],
                },
            })

        lecture.delete()
        return JsonResponse({
            'success': True,
            'lecture_pin': pin,
        })


class LectureTopics(View):
    def get(self, request, pin=None):
        """ Read list of lecture topics """
        topic_list = models.LectureTopic.objects.filter(lecture__pin=pin).order_by('order')
        return JsonResponse({
            'success': True,
            'lecture_topics': [topic.as_dict() for topic in topic_list],
        })

    @method_decorator(login_required)
    def post(self, request, pin=None):
        """ Create lecture topic """
        # TODO remember to check if user has access (owner) to course
        form = forms.LectureTopicForm(request.POST)
        if form.is_valid():
            try:
                lecture = models.Lecture.objects.get(pin=pin, course__user=request.user)
            except models.Lecture.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'errors': {
                        'message': ['Lecture with PIN does not exist for this user'],
                    },
                })

            topic = form.save(commit=False)
            topic.lecture = lecture
            topic.save()
            return JsonResponse({
                'success': True,
                'lecture_topic': topic.as_dict(),
            }, status=201)

        # Form is invalid so return errors
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        })


class LectureTopicDetails(View):
    def get(self, request, pin=None, topic_id=None):
        """ Read lecture topic details """
        try:
            topic = models.LectureTopic.objects.get(id=topic_id, lecture__pin=pin)
        except models.LectureTopic.DoesNotExist:
            return JsonResponse({
                'success': False,
                'errors': {
                    'message': ['Topic ID does not exist for this lecture'],
                },
            })

        return JsonResponse({
            'success': True,
            'lecture_topic': topic.as_dict(),
        })

    @method_decorator(login_required)
    def post(self, request, pin=None, topic_id=None):
        """ Update lecture topic """
        # TODO remember to check if user has access (owner) to course
        form = forms.LectureTopicForm(request.POST)
        if form.is_valid():
            try:
                topic = models.LectureTopic.objects.get(
                    id=topic_id,
                    lecture__pin=pin,
                    lecture__course__user=request.user
                )
            except models.LectureTopic.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'errors': {
                        'message': ['Topic ID does not exist for this lecture and user'],
                    },
                })

            topic.title = form.cleaned_data['title']
            topic.order = form.cleaned_data['order']
            topic.save()
            return JsonResponse({
                'success': True,
                'lecture_topic': topic.as_dict(),
            })

        # Form is invalid so return errors
        return JsonResponse({
            'success': False,
            'errors': form.errors,
        })

    @method_decorator(login_required)
    def delete(self, request, pin=None, topic_id=None):
        """ Delete lecture topic """
        # TODO remember to check if user has access (owner) to course
        try:
            topic = models.LectureTopic.objects.get(
                id=topic_id,
                lecture__pin=pin,
                lecture__course__user=request.user
            )
        except models.LectureTopic.DoesNotExist:
            return JsonResponse({
                'success': False,
                'errors': {
                    'message': ['Topic ID does not exist for this lecture and user'],
                },
            })

        topic.delete()
        return JsonResponse({
            'success': True,
            'lecture_topic_id': topic_id,
        })


class LectureTopicUnderstanding(View):
    def post(self, request, pin=None, topic_id=None):
        """ Create opinion on lecture topic understanding """
        form = forms.TopicUnderstandingForm(request.POST)
        if form.is_valid():
            try:
                topic = models.LectureTopic.objects.get(id=topic_id, lecture__pin=pin)
            except models.LectureTopic.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'errors': {
                        'message': ['Topic ID does not exist for this lecture'],
                    },
                })

            if form.cleaned_data['understanding']:
                topic.understanding += 1
            else:
                topic.understanding -= 1
            topic.save()
            return JsonResponse({
                'success': True,
                'lecture_topic': topic.as_dict(),
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
            try:
                lecture = models.Lecture.objects.get(pin=pin)
            except models.Lecture.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'errors': {
                        'message': ['Lecture does not exist'],
                    },
                })

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
        try:
            question = models.Question.objects.get(id=question_id, lecture__pin=pin)
        except models.Lecture.DoesNotExist:
            return JsonResponse({
                'success': False,
                'errors': {
                    'message': ['Question ID does not exist for this lecture'],
                },
            })

        question.votes += 1
        question.save()
        return JsonResponse({
            'success': True,
            'question': question.as_dict(),
        })


class LecturePace(View):
    def get(self, request, pin=None):
        """ Read digest of lecture pace opinions """
        try:
            lecture = models.Lecture.objects.get(pin=pin)
        except models.Lecture.DoesNotExist:
            return JsonResponse({
                'success': False,
                'errors': {
                    'message': ['Lecture does not exist'],
                },
            })

        return JsonResponse({
            'success': True,
            'lecture': lecture.as_dict(),
        })

    def post(self, request, pin=None):
        """ Create opinion on lecture pace """
        form = forms.PaceForm(request.POST)
        if form.is_valid():
            try:
                lecture = models.Lecture.objects.get(pin=pin)
            except models.Lecture.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'errors': {
                        'message': ['Lecture does not exist'],
                    },
                })

            if form.cleaned_data['pace']:
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
        try:
            lecture = models.Lecture.objects.get(pin=pin)
        except models.Lecture.DoesNotExist:
            return JsonResponse({
                'success': False,
                'errors': {
                    'message': ['Lecture does not exist'],
                },
            })

        return JsonResponse({
            'success': True,
            'lecture': lecture.as_dict(),
        })

    def post(self, request, pin=None):
        """ Create opinion on lecture volume """
        form = forms.VolumeForm(request.POST)
        if form.is_valid():
            try:
                lecture = models.Lecture.objects.get(pin=pin)
            except models.Lecture.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'errors': {
                        'message': ['Lecture does not exist'],
                    },
                })

            if form.cleaned_data['volume']:
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
                    'errors': {
                        'message': ['Course with this title already exists'],
                    },
                })

            course = form.save(commit=False)
            course.user = request.user
            course.save()
            return JsonResponse({
                'success': True,
                'course': course.as_dict()
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
        try:
            course = models.Course.objects.get(id=course_id, user=request.user)
        except models.Course.DoesNotExist:
            return JsonResponse({
                'success': False,
                'errors': {
                    'message': ['Course ID does not exist for this user'],
                },
            })

        return JsonResponse({
            'success': True,
            'course': course.as_dict(),
        })

    @method_decorator(login_required)
    def post(self, request, course_id):
        """ Update course details for course_id """
        # TODO remember to check if user has access (owner) to course
        form = forms.CourseForm(request.POST)
        if form.is_valid():
            try:
                course = models.Course.objects.get(id=course_id, user=request.user)
            except models.Course.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'errors': {
                        'message': ['Course ID does not exist for this user'],
                    },
                })

            course.title = form.cleaned_data['title']
            return JsonResponse({
                'success': True,
                'course': course.as_dict(),
            })

        return JsonResponse({
            'success': False,
            'errors': form.errors,
        })

    @method_decorator(login_required)
    def delete(self, request, course_id):
        """ Delete course with course_id """
        # TODO remember to check if user has access (owner) to course
        try:
            course = models.Course.objects.get(id=course_id, user=request.user)
        except models.Course.DoesNotExist:
            return JsonResponse({
                'success': False,
                'errors': {
                    'message': ['Course ID does not exist for this user'],
                },
            })

        course.delete()
        return JsonResponse({
            'success': True,
            'course_id': course_id,
        })


class CourseLectures(View):
    @method_decorator(login_required)
    def get(self, request, course_id):
        """ Read list of latest lectures for course_id """
        # TODO remember to check if user has access (owner) to course
        lecture_list = models.Lecture.objects.filter(
            course__id=course_id, course__user=request.user).order_by('-start_datetime')
        return JsonResponse({
            'success': True,
            'lectures': [lecture.as_dict() for lecture in lecture_list],
        })

    @method_decorator(login_required)
    def post(self, request, course_id):
        """ Create new lecture for course_id """
        # TODO remember to check if user has access (owner) to course
        try:
            course = models.Course.objects.get(id=course_id, user=request.user)
        except models.Course.DoesNotExist:
            return JsonResponse({
                'success': False,
                'errors': {
                    'message': ['Course ID does not exist for this user'],
                },
            })

        form = forms.LectureForm(request.POST)
        if form.is_valid():
            lecture = form.save(commit=False)
            lecture.course = course

        else:
            lecture_count = models.Lecture.objects.filter(course__id=course_id, course__user=request.user).count()
            lecture = models.Lecture(
                course=course,
                title=str(request.user).split('@')[0] + " - " + str(course.title) + " - " + str(lecture_count + 1)
            )

        lecture.save()
        return JsonResponse({
            'success': True,
            'lecture': lecture.as_dict(),
        }, status=201)
