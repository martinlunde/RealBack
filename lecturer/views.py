
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Course

@login_required  # TODO check for group instead
def front_page(request):
    """ Lecturer main page """
    course_list = Course.objects.filter(user=request.user)
    # TODO pass in list of existing lectures for this user
    return render(request, 'lecturer/front_page.html', {'courses':course_list})


# def login(request):
#     """ Users are redirected here if login is required """
#     # TODO pass in login form
#     return render(request, 'lecturer/login_page.html', {})


@login_required  # TODO check for group instead
def new_lecture(request):
    """ Create new lecture view """
    # TODO pass in lecture form
    return render(request, 'lecturer/new_lecture.html', {})
