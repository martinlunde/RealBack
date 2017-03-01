
from django.shortcuts import render, redirect
from lecturer import models as lecturer_models


def index(request):
    """ Main index page for RealBack """
    # TODO pass in PIN login form
    return render(request, 'attendee/index.html', {})


# def joined(request):
#     """ Temp demo stuff """
#     # TODO check session OK
#     # TODO pass in lecture name
#     # return render(request, 'attendee/joined.html', {})
#     pass


def about_us(request):
    return render(request, 'attendee/about_us.html', {})


def attend_lecture(request, pin=None):
    if pin is None:
        return redirect('index')

    try:
        lecture = lecturer_models.Lecture.objects.get(pin=pin)
    except lecturer_models.Lecture.DoesNotExist:
        # TODO some kind of sane error message
        return redirect('index')

    return render(request, 'attendee/lecture.html', {'lecture_name': lecture.title})
