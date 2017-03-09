
from django.shortcuts import render
from realback_api import forms


def index(request):
    """ Main index page for RealBack Attenders """
    # TODO necessary forms and info
    question_form = forms.QuestionForm()
    return render(request, 'attendee/index.html', {'question_form': question_form})


def about_us(request):
    return render(request, 'attendee/about_us.html', {})
