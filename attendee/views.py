
from django.shortcuts import render


def index(request):
    """ Main index page for RealBack Attenders """
    # TODO necessary forms and info
    return render(request, 'attendee/index.html', {})


def about_us(request):
    return render(request, 'attendee/about_us.html', {})
