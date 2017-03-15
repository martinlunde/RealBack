
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from realback_api import models, forms


@login_required
def front_page(request):
    """ View lecturer front page """
    # TODO forms
    course_form = forms.CourseForm()
    return render(request, 'lecturer/front_page.html', {
        'course_form': course_form,
    })
