
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from realback_api import models, forms


@login_required
def front_page(request):
    """ View lecturer front page """
    # TODO forms
    course_form = forms.CourseForm()
    lecture_form = forms.LectureForm()
    topic_form = forms.LectureTopicForm()
    return render(request, 'lecturer/front_page.html', {
        'course_form': course_form,
        'lecture_form': lecture_form,
        'topic_form': topic_form,
    })
