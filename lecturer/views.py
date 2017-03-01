
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models


@login_required  # TODO check for group instead
def front_page(request):
    """ Lecturer main page """
    course_list = models.Course.objects.filter(user=request.user)
    # TODO pass in list of existing lectures for this user

    return render(request, 'lecturer/front_page.html', {'course_list': course_list})


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
    if request.method == "POST":
        form = forms.NewLectureForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lecturer:front_page')

    else:
        form = forms.NewLectureForm()

    return render(request, 'lecturer/new_lecture.html', {'form': form})


@login_required  # TODO check for group instead
def course(request, course=None):
    if course is None:
        return redirect('front_page')

    try:
        # TODO change this or make course title unique on a per user basis
        course_current = models.Course.objects.get(title=course, user=request.user)
        lecture_list = models.Lecture.objects.filter(course__title=course)
    except:
        # TODO some kind of sane error message
        return redirect('front_page')

    return render(request, 'lecturer/course.html', {'course_current': course_current, 'lecture_list': lecture_list})


@login_required  # TODO check for group instead
def lecture(request, course=None, lecture=None):
    if course is None or lecture is None:
        return redirect('front_page')

    try:
        # TODO change this or make course title is unique on a per user basis
        # and lecture title is unique on a per course basis
        lecture_current = models.Lecture.objects.get(title=lecture, course__title=course)
    except:
        # TODO some kind of sane error message
        return redirect('front_page')

    return render(request, 'lecturer/lecture.html', {'lecture_current': lecture_current})
