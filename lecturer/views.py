
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required  # TODO check for group instead
def front_page(request):
    """ Lecturer main page """
    # TODO pass in list of existing lectures for this user
    # return render(request, 'templates/lecturer/front_page.html', {})
    pass


# def login(request):
#     """ Users are redirected here if login is required """
#     # TODO pass in login form
#     return render(request, 'templates/lecturer/login_page.html', {})


@login_required  # TODO check for group instead
def new_lecture(request):
    """ Create new lecture view """
    # TODO pass in lecture form
    # return render(request, 'templates/lecturer/new_lecture.html', {})
    pass
