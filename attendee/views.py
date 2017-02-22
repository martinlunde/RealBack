
from django.shortcuts import render


def index(request):
    """ Main index page for RealBack """
    # TODO pass in PIN login form
    return render(request, 'attendee/index.html', {})


def joined(request):
    """ Temp demo stuff """
    # TODO check session OK
    # TODO pass in lecture info
    # return render(request, 'attendee/joined.html', {})
    pass
