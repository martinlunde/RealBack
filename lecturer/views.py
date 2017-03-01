
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from . import forms, models


def get_courses_and_lectures(request):
    courses = models.Course.objects.filter(user=request.user)
    lecture_list = models.Lecture.objects.filter(course__user=request.user)
    return courses, lecture_list


@login_required
def create_lecture_in_course(request):
    """ Create new lecture in an existing course,
    and creates a course if course does not exist"""
    if request.method == "POST":
        form = forms.NewOverallForm(request.POST)
        if form.is_valid():
            value = form.cleaned_data['title']
            if not models.Course.objects.filter(title=value, user=request.user):
                c = models.Course(title=value, user=request.user)
                c.save()
            else:
                c = models.Course.objects.get(title=value, user=request.user)

            t = len(models.Lecture.objects.filter(course__title=value, course__user=request.user))
            l = models.Lecture(course=c, title=str(request.user) + "_" + str(c.title) + "_" + str(t + 1))
            l.save()
            return redirect('lecturer:front_page')
    else:
        form = forms.NewOverallForm()
        courses, lectures = get_courses_and_lectures(request)

    return render(request, 'lecturer/front_page.html', {'form': form, 'courses': courses, 'lectures': lectures})


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
