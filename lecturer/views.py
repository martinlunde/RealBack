
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def front_page(request):
    # if already logged in:
    pass
    # else serve login page
    # return render(request, 'templates/lecturer/login_page.html', {})


def login(request):
    return render(request, 'templates/lecturer/login_page.html', {})
