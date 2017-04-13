
from django.shortcuts import render
from realback_api import forms


def index(request):
    """ Main index page for RealBack Attenders """
    # TODO necessary forms and info
    question_form = forms.QuestionForm()
    volume_form = forms.VolumeForm()
    pace_form = forms.PaceForm()
    return render(request, 'attendee/index.html', {
        'question_form': question_form,
        'volume_form': volume_form,
        'pace_form': pace_form,
        'topic_understanding_form': forms.TopicUnderstandingForm(),
    })


def about_us(request):
    return render(request, 'attendee/about_us.html', {})
