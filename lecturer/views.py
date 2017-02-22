
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms


@login_required  # TODO check for group instead
def front_page(request):
    """ Lecturer main page """
    # TODO pass in list of existing lectures for this user
    return render(request, 'lecturer/front_page.html', {})


@login_required
def new_course(request):
    """ Create new course """
    if request.method == 'POST':
        form = forms.NewCourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            return redirect('lecturer:front_page')

    else:
        form = forms.NewCourseForm()

    return render(request, 'lecturer/new_course.html', {'form': form})


@login_required  # TODO check for group instead
def new_lecture(request):
    """ Create new lecture """
    if request.method == 'POST':
        form = forms.NewLectureForm(request.POST)
        if form.is_valid():
            lecture = form.save(commit=False)
            # TODO find correct course and put in lecture
            # lecture.course = course
            lecture.save()
            return redirect('lecturer:front_page')

    else:
        form = forms.NewLectureForm()

    return render(request, 'lecturer/new_lecture.html', {'form': form})
